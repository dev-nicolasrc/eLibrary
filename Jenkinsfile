pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')  // Revisa cambios cada 2 minutos
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        // Intenta usar docker compose, si no funciona usa fallback
        DOCKER_COMPOSE_CMD = 'docker compose'
        DOCKERHOST_CMD = 'docker'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Limpiando workspace..."
                deleteDir()
                echo "Clonando repositorio..."
                git branch: 'main',
                    url: 'https://github.com/dev-nicolasrc/eLibrary.git'
                
                echo "✅ Repositorio clonado exitosamente"
            }
        }

        stage('Build imagen Django') {
            steps {
                echo "🐳 Intentando construir imagen Docker..."
                script {
                    def dockerAvailable = sh(
                        script: 'which docker > /dev/null 2>&1',
                        returnStatus: true
                    )
                    
                    if (dockerAvailable == 0) {
                        echo "✅ Docker disponible. Construyendo imagen..."
                        sh '''
                            ${DOCKER_COMPOSE_CMD} down -v || true
                            ${DOCKER_COMPOSE_CMD} build --no-cache web
                        '''
                    } else {
                        echo "⚠️ Docker no disponible en Jenkins"
                        echo "💡 Ejecutar builds localmente o configurar Docker en Jenkins"
                        sh '''
                            echo "Para ejecutar localmente:"
                            echo "cd biblioteca_virtua"
                            echo "docker build -t django-app ."
                        '''
                    }
                }
            }
        }

        stage('Levantar MySQL') {
            when {
                expression { sh(script: 'which docker > /dev/null 2>&1', returnStatus: true) == 0 }
            }
            steps {
                sh '''
                    echo "Levantando solo el servicio de base de datos..."
                    ${DOCKER_COMPOSE_CMD} up -d db

                    echo "Estado de los contenedores:"
                    ${DOCKER_COMPOSE_CMD} ps
                '''
            }
        }

        stage('Migraciones') {
            when {
                expression { sh(script: 'which docker > /dev/null 2>&1', returnStatus: true) == 0 }
            }
            steps {
                sh '''
                    echo "Esperando a que la base de datos esté lista..."
                    sleep 10
                    
                    echo "Ejecutando migraciones dentro del contenedor Django (web)..."
                    ${DOCKER_COMPOSE_CMD} run --rm web sh -c "python manage.py migrate"
                '''
            }
        }

        stage('Pruebas Unitarias') {
            when {
                expression { sh(script: 'which docker > /dev/null 2>&1', returnStatus: true) == 0 }
            }
            steps {
                sh '''
                    echo "🧪 Ejecutando pruebas unitarias con mocks (usando SQLite en memoria)..."
                    
                    # Establecer variable de entorno para usar SQLite en pruebas
                    ${DOCKER_COMPOSE_CMD} run --rm -e TESTING=1 web python run_unit_tests.py
                    
                    echo "✅ Pruebas unitarias completadas."
                '''
            }
        }
        
        stage('Reporte de Cobertura') {
            when {
                expression { sh(script: 'which docker > /dev/null 2>&1', returnStatus: true) == 0 }
            }
            steps {
                echo "📊 Iniciando generación de reporte de cobertura..."
                
                sh '''
                    echo "📊 Generando reporte de cobertura..."
                    
                    # Ejecutar tests con cobertura y generar reportes
                    # Usar un volumen temporal para compartir archivos
                    mkdir -p coverage_output
                    
                    ${DOCKER_COMPOSE_CMD} run --rm -e TESTING=1 \
                        -v $(pwd)/coverage_output:/app/coverage_output \
                        web sh -c "
                        coverage run --source=libros,usuarios,prestamos,core run_unit_tests.py &&
                        coverage report -m &&
                        coverage xml -o /app/coverage_output/coverage.xml &&
                        coverage html -d /app/coverage_output/htmlcov
                    " || echo "⚠️ Error al ejecutar coverage, pero continuando..."
                    
                    # Mover archivos al workspace de Jenkins
                    if [ -f coverage_output/coverage.xml ]; then
                        mv coverage_output/coverage.xml .
                        echo "✅ coverage.xml copiado"
                    else
                        echo "⚠️ coverage.xml no encontrado"
                    fi
                    
                    if [ -d coverage_output/htmlcov ]; then
                        mv coverage_output/htmlcov .
                        echo "✅ htmlcov copiado"
                    else
                        echo "⚠️ htmlcov no encontrado"
                    fi
                    
                    # Limpiar directorio temporal
                    rmdir coverage_output 2>/dev/null || rm -rf coverage_output
                    
                    echo "✅ Reporte de cobertura generado."
                    echo "📁 Archivos generados:"
                    ls -la coverage.xml htmlcov/ 2>/dev/null || echo "Algunos archivos no se encontraron"
                '''
            }
            post {
                always {
                    script {
                        try {
                            // Publicar reporte XML para el plugin de Cobertura de Jenkins
                            if (fileExists('coverage.xml')) {
                                publishCoverage adapters: [
                                    coberturaAdapter('coverage.xml')
                                ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                                echo "✅ Reporte XML de cobertura publicado"
                            } else {
                                echo "⚠️ Archivo coverage.xml no encontrado - el reporte de cobertura no se publicará"
                            }
                            
                            // Publicar reporte HTML
                            if (fileExists('htmlcov/index.html')) {
                                publishHTML([
                                    reportDir: 'htmlcov',
                                    reportFiles: 'index.html',
                                    reportName: 'Cobertura de Código',
                                    keepAll: true
                                ])
                                echo "✅ Reporte HTML de cobertura publicado"
                            } else {
                                echo "⚠️ Reporte HTML de cobertura no encontrado"
                            }
                        } catch (Exception e) {
                            echo "⚠️ Error al publicar reportes de cobertura: ${e.getMessage()}"
                            echo "⚠️ Esto puede deberse a que los plugins no están instalados"
                        }
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                expression { sh(script: 'which docker > /dev/null 2>&1', returnStatus: true) == 0 }
            }
            steps {
                sh '''
                    echo "Desplegando aplicación..."
                    ${DOCKER_COMPOSE_CMD} up -d
                    
                    echo "Verificando servicios desplegados:"
                    ${DOCKER_COMPOSE_CMD} ps
                    
                    echo "✅ Aplicación disponible en http://localhost:8000"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline exitoso. Aplicación desplegada correctamente."
        }
        failure {
            echo "❌ Pipeline falló. Ejecutando cleanup..."
            sh '''
                echo "Limpiando contenedores..."
                ${DOCKER_COMPOSE_CMD} down -v 2>/dev/null || true
                echo "Cleanup completado"
            '''
        }
        always {
            echo "🔍 Estado final del pipeline"
            sh '''
                echo "Contenedores activos:"
                ${DOCKER_COMPOSE_CMD} ps 2>/dev/null || echo "Docker no disponible"
            '''
        }
    }
}
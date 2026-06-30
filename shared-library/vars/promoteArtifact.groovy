def call(Map config = [:]) {
    def artifact = config.artifact ?: error('artifact is required')
    def version = config.version ?: error('version is required')
    def fromRepo = config.fromRepo ?: 'docker-local'
    def toRepo = config.toRepo ?: 'docker-release'

    echo "Promoting ${artifact}:${version} from ${fromRepo} to ${toRepo}"
    sh """
        ./scripts/jfrog-promote.sh \
            --artifact ${artifact} \
            --version ${version} \
            --from ${fromRepo} \
            --to ${toRepo}
    """
}

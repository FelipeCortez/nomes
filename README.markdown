A table of Brazilian names sorted by popularity.

To obtain the data, I used the internal API from the [Nomes no Brasil web app](https://censo2010.ibge.gov.br/nomes/). I found the database has been made public afterwards [here](http://www.consultaesic.cgu.gov.br/busca/dados/Lists/Pedido/Item/displayifs.aspx?List=0c839f31%2D47d7%2D4485%2Dab65%2Dab0cee9cf8fe&ID=645553&Source=http%3A%2F%2Fwww%2Econsultaesic%2Ecgu%2Egov%2Ebr%2Fbusca%2FSitePages%2Fresultadopesquisa%2Easpx%3Fk%3Dnomes%2520OrgaoVinculado%253A%2522IBGE%2520%25E2%2580%2593%2520Funda%25C3%25A7%25C3%25A3o%2520Instituto%2520Brasileiro%2520de%2520Geografia%2520e%2520Estat%25C3%25ADstica%2522&Web=88cc5f44%2D8cfe%2D4964%2D8ff4%2D376b5ebb3bef)

## Running

Clone SQLite-Levenshtein with `git submodule update --init`

Build the Docker image with `docker image build -t nomes .`

Run a development environment with `docker run -e FLASK_ENV=development -p 5000:5000 nomes`

Run a production environment with `docker run -e FLASK_ENV=production -p 5000:5000 nomes`

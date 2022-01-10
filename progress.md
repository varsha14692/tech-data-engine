# Progress
# Progress... 6/01/2022
 * Went through project README.md file and understood the project and requirement
# Progress... 7/01/2022
* Studied about docker
# Progress... 8/01/2022
 * Installed docker desktop https://github.com/docker/rootfs.git#container:docker
 * Go to Dev Environments --> create --> Get started --> Enter GIT repository URL https://github.com/varsha14692/tech-data-engine.git
 * Dev Envronment setup done 
 * Opened CLI and executed docker-compose up in com.docker.devenvironments.code folder
 * 'articles' and 'users' tables are available in the postgres database
 * Challange 1 : I was not able to find blob data.
 * Resolution : I figured out that there are 2 volumes, database and data storage.
 * static data : 'articles' and 'users' are available in database as well as in data storage. 
 * dynamic data : 'purchases' was available only in data storage in JSON format.
 # Progress... 9/01/2022
 * Started working on code change.
 * Modified purchases.py and data.py in order to insert the 'purchases' data in postgres.
 * Challange 2 : While inserting the data into 'purchases' table, error got triggered "ON CONFLICTS  (id) DO NOTHING"
 * Resolution : There were multiple article ids for one purchase id and unique key was not available, so I added a new column 'document id' which contains purchase JSON document id and can be repetitative as there may be more than one article id associated with one purchase document id.
 * Also, added one unique id in puchases table using UUID.
 * Now, 'purchases' data is in querable format and joins/sql functions can be applied on this inserted data. 
# Progress... 10/01/2022
 * Went through the code changes again and pushed the code changes to git repository.
 * Code changes are available at git hub repo " https://github.com/varsha14692/tech-data-engine.git "
 * Since some of the aticles and users data columns in blob documents are different and not accepted in purchases, therefore few of the purchases JSON data is not getting inserted in 'purchases' table. This would require some more effort and daa cleansing at code level.
 
 * Unresolved : Access denied to file which count number of purchases using file count_purchase_files.sh

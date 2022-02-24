# Carto-test approach
--------------------
This solution is an approach to a data engenieer challenge. The challenge cosists of  building a plan to identify 
5 groups of restaurants in the Metropolitan Area of Madrid for a brand new delivery app. Each group will consist 
of a set of restaurants, allowing the company to optimize delivery times.

## An extra ball

The challenge is built in a docker-compose config solution files. Both of the files `dockerfile` and `docker-compose.yml` 
creates an enviroment with a flask app local hosted an accessed by port 4000. In other to connect to bigQuery and google cloud 
an service account credential is needed so you need to overwrite the current `gc_credentials.json`. 

## Orchestator

1. For the execution of this test, the local path contanin the solution must be updated inside the `carto-test.ipynb` :
2. The first approach was made on KMEANS model for clustering by labels
3. However many labels were null so an BDSCAND model tries to cluster a second soltion, also handle outliers. So a new column was create in the csv result file. 
4. Finally, the iterations are plotted using CARTOframe functions. 

# PINTA

### REST API

**Recommend Articles**

URL : [http://127.0.0.1:5000/recommend/article](http://127.0.0.1:5000/recommend/article)

Type : POST

*Request*

```json
{
	"_id":33
}
```

*Response*

```json
{
    "recommends": [
        {
            "_id": 3825,
            "score": "0.9625477",
            "title": "Review: Killed Whole-Cell Oral Cholera Vaccine Efficacious"
        },
        {
            "_id": 1479,
            "score": "0.9583732",
            "title": "Serum Trypsinogen Levels Down in Type 1 Diabetes"
        },
        {
            "_id": 1424,
            "score": "0.9522217",
            "title": "Type 1 Diabetes Tied to Gut Inflammation, Microbiota"
        },
        {
            "_id": 1845,
            "score": "0.9518573",
            "title": "Complication Rates Often Higher in Youth With T2DM Versus T1DM"
        },
        {
            "_id": 4855,
            "score": "0.9493152",
            "title": "Colorectal Lesion Frequency Increases at Age 45"
        }
    ],
    "source": {
        "_id": 33,
        "title": "More Diabetes-Associated, Non-Associated Autoantibodies in T1D"
    },
    "status": "success"
}
```

**Retrain Model**

_URL_ : [http://127.0.0.1:5000/recommend/retrain?num_topics=64&refresh_dataset=true&force=false](http://127.0.0.1:5000/recommend/retrain?num_topics=64&refresh_dataset=true&force=false)

_Type_ : GET

_About Parameters_
> num_topics=64 
> #number of topics 
> 
> refresh_dataset=true
> #refresh dictionary, corpus, index e.t.c
> 
> force=false 
> #fetch entirely fresh dataset from database
> 
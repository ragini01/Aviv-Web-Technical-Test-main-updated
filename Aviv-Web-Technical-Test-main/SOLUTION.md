# AVIV technical test solution

I've applied for a back-end position. Hence, my target was to focus on BACKEND part of this Listing Application.

### Technology
Python-Flask

### Implementation
 
Main README.md file has the overall context to understand the ask of this challange. But, before jumping to the implementation of the new endpoint to fetch and display the pricing history of a listing, I've walked through the codebase to understand the source code structure, overall architecture and design of the project and the API designs and schema. Implementation includes,

#### Adapters Level Changes

**DB Schema Changes**
 1. To maintain/store pricing history, created a new table `price_history` in db and used `id` from listing table as refrence.
 2. Since, Mocked data should not be used as the API response, populated data in db by adding `insert` statment.

 **Model Changes**
 1. Added new model class `PriceHistoryModel`
 2. Added new mapping function inside `mappers.py`
 3. New function `get_prices` added to get the pricing history of listings inside `sql_alchemy_listing_repository.py` file

 #### Domain Level Changes
 1. Created new use case `retrieve_listing_prices.py` to retrieve listing prices.
 2. Added the newly created use case in the `registry.py`

 #### API/Controller Level Changes
 1. Added logic to the new endpoint route `/listings/<int:id_>/prices`

 ### Assumptions

 I would like to highlight all my assumptions and findings here while working on this project's task. At First, I should talk about the overall architecture and design of the project. As mentioned in the docs, this project is built using `Hexagonal Architecture`. I had no past working experience with this architecture design. So, I spent my initial few hours undersatnding this architectural pattern and then understanding the decision of choosing this model for this project. In my understanding, I put myself in a strong favor why Hexagonal is used here. Here, are the points,
 1. Separation of User-side, buisness logic and Server-side
    This separation means we are actually separating the problems and hence can focus on a single logic at a time. Also, by this separation we put our buisness logic at the forefront of our code and by doing this buisness logic can be isolated is a module/directory to make it explicit to the developers and then can be defined, tested and refined without taking on the cognitive load of the rest of the application/program. And, finally in terms of automated tests, we can initiate and drive tests individually for buisness logic, integration of user side and buisness and then integration between buisness and server-side independentally.
 2. Everything depends here on the buisness logic, the buisness logic doesn't depend on anything 
 3. Boundaries are isolated with interfaces(Adapters and ports in this case)
 4. At the runtime, to understand the Hexagonal architecture this is how the overall applications gets started,
    - Go outside of the Hexagon, to the right and intantiate the right side adapter(server-side) which will be the database in our case
    - Instantiate the Hexagon means the buisness logic that will be driven by the application
    - Instantiate the left side adapter i.e. user-side which will be asking to go inside the hexagon
 5. On a braoder scale, I feel the decisison to choose Hexagonal architecture is to use `DDD(Dromain Driven Design)` mindset. Because at the moment, we have limited inputs and ports where one of them is API in the user-side. And, in the server side we are saving everything to db. But what if tomorrow we replace the server-side as well with the API which basically means input of the application is an API and output might also be calling an API then we can go one staep towards `DDD` approach and think each of the Hexagon as one single domain and try connecting or expanding Hexagons with another one where all will be specifically designed domain specific.

 Secondaly, I'd be discussing my approach and time estimation for this task here. As mentioned above, I started my actual work by doing a minimal required research about the code architecture. Then, I colned the source code and moved towards setting up the project locally, building and running it before making any changes. I again spent little more time here to do the setup locally as I found a use of `Make` tool in this project. I never automated any of my python stuffs using `Make` tool and created a `Makefile`. So, I had to setup the tool and then go through the Makefile to understand how and what all steps are automated. The set/asked target to complete the task was between `90-180 minutes`, where I've spent my overall time from understanding to the final implementation was truely beyond this time frame. Implementation took almost around 3:30 hrs but overall unsersatnding and setup allowed me to spent more time (Total around 6-7 hrs) than asked here.


## Notes

Write here notes about your implementation choices and assumptions.

## Questions

This section contains additional questions your expected to answer before the debrief interview.

- **What is missing with your implementation to go to production?**

1. First thing which I can think of missing from my current implementation is the more test case scenarios and a reframed acceptance criteria and then adding them in the code.
2. Also, I believe we are currently using open source libraries from python and going further that'll be increasing in numbers, so the security scanning where checking the vulnerabilities and there severity level should take place.
3. I would also like to handle all the unhealthy states of my API's which means there can be an extra end point doing `HealthCheck` and would be adding all the instruction to wake up this endpoint in the dockerfile.
4. I would also consider python `Web Server Gateway Interface(WSGI)` for production to avoid development server or debugger to run in a prod environment.

- **How would you deploy your implementation?**

I can proceed for the deployment `only if my changes are worth it`. After that, may be the next step could be thinking about the `Scope Management` when we work in Agile. Once I get clarity on these 2 points, next step would be following a `deployment plan` and then go through the flow of the plan.

- **If you had to implement the same application from scratch, what would you do differently?**

 May be I can start the development of the project by given a chance from scratch, then by considering the buisness goal of AVIV and it's current market would like to design the project architecture as `microservices` which will be very close to the current approach where we are focused and reliable on separation of concerns and DDD approach. Again the communication between my componenets/microservices would then be acheived by REST api's. Regarding the technology of the API, I might switch to FastAPI framework rather than Flask.  

 Moving forward, I see there is a heavy dependency or can say db realted operations in real estate applications. So, my concern and consideration would be on db operations. I would think of handling such operations smoothly and also focus on the data consistency. Some techniques like db caching or may be creating a replica of read operations, wisely formaing the db queries and choosing may be a SQLAlchemy API instead of ORM.

 Following to the current design, I would also like to dockerize my python application the way it's done currently where lot of standards have been considered wether it's a practice to wisely take decisions on selecting base images for the python project in terms of size and minimal functionality match or taking decisions on running containerized python applications with `least possible privilege`.

 Moving to the next step, I will try to set up `CI/CD pipeline` either using automatic tools or by using github actions. This will be done basically to automate the build, test and deployment processes. Also, given an option I would like to choose a cloud provider to host the application may be(AWS). Then, will choose orchestartion tools as well to manage my containers in production like Kubernetes. Then at last, may be I can find and come up with some effective and best suited montitoring and centralized logging system tools (may be Grafana or Prometheus) by considering my code architecture as Microservices. 

- **The application aims at storing hundreds of thousands listings and millions of prices, and be accessed by millions of users every month. What should be anticipated and done to handle it?**
 
To answer this question, My 1st approach could be thinking of an `efficient and optimized data storage system and techniques` which can cover numerous decision factors such as having some production db backups or Disaster recovery, Caching techniques at several stages within application including DB side and Auto-scaling techniques.
Secondaly, I can think of Horizontal scaling either by using some common techniques like using Load balancers or take a cloud native solutions like AWS.
Then, last point would be implementing robust monitoring tools and regularly analyze logs and server performances to identify the bottlenecks.

  NB : You can update the [given architecture schema](./schemas/Aviv_Technical_Test_Architecture.drawio) by importing it
  on [diagrams.net](https://app.diagrams.net/) 

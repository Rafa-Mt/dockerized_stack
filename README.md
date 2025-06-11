# Deployment architecture with docker

### Todos:
 - [x] Define Postgres data model
 - [x] Define Redis schema
 - [ ] Develop Backend Main Server _(python)_
   - [ ] Auth 
     - [ ] Sessions _(with redis state)_
     - [ ] Sign in & Sign up funcionality
     - [ ] Cookies jwt session token
     - [ ] Routes
   - [ ] Business
     - [ ] Routes
     - [ ] Microservice client
 - [ ] Develop Heavy Computation Microservice _(rust)_
   - [ ] Define behavior
   - [ ] Declare protobuffers
   - [ ] Microservice server
 - [ ] Develop Mailer Server _(language to be defined, probably rust)_
   - [ ] Resend integration
   - [ ] Declare protobuffers
   - [ ] Microservice server
 - [ ] Define reverse proxy behavior _(traefik)_

### Docker architecture: 

![](deployment_model.png)
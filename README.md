# Deployment architecture with docker

### Docker services
- `client`: Frontend written in _Vue_ with _Typescript_ and built with _vite_ and _nodejs_
- `backend_server`: Backend written in _Python_ using the _Flask_ framework
- `heavy_computation`: _Rust_ microservice for performing fast and eficcient heavy calculations
- `mailer`: _`language to be defined`_ microservice for mailing with _Resend_ api
- `redis`: Cache database for session storage
- `postgres`: Main database for data storage

### Funcionality

Basic user and post CRUD with some heavy operations (to be defined) and posting notifications via email

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
 - [ ] Develop frontend client _(vue ts)_
   - [ ] Auth view
       - [ ] Login component
       - [ ] Register component
   - [ ] Business view
     - [ ] Create post component
     - [ ] View post component
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
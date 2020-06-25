import models
from typing import List
from fastapi import FastAPI, Request, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from pydantic import BaseModel 
from models import State
import schemas
from sqlalchemy.orm import Session
import COVID19Py
from starlette.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

covid = COVID19Py.COVID19()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


class StateRequest(BaseModel):
	state: str

def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()

@app.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
	"""
	Displays COVID-19 Live Data Homepage Dashboard
	"""
	return RedirectResponse(url="/docs/")
	#countries = db.query(State).all()

	#CHANGE THIS!!!!!!!!!! DONT HAVE THE JINJA2 TEMPLATES ANYMORE
	#return templates.TemplateResponse("dashboard.html", {
		#"request": request,
		#"countries": countries
	#})

def populate_data():
	db = SessionLocal()
	countries = covid.getLocations(rank_by='deaths')
	for country in countries:
		db_record = models.State(
        id = country['id'],
    	country = country['country'],
    	country_code = country['country_code'],
    	population = country['country_population'],
    	last_updated = country['last_updated'],
    	confirmed = ((country['latest'])['confirmed']),
    	deaths = ((country['latest'])['deaths']),
    	recovered = ((country['latest'])['recovered'])
        )
		db.add(db_record)
	db.commit()

@app.get("/records/", response_model=List[schemas.Record])
def show_records(db: Session = Depends(get_db)):
	populate_data()
	records = db.query(models.State).all()
	return records

def fetch_data(id: str):
	db = SessionLocal()

	country = db.query(State).filter(State.id == id).first()

	state_data = covid.get_status_by_country_name(country.state)

	country.id = state_data['id']
	
	country.state = state_data['country'].capitalize()
	
	country.confirmed = state_data['confirmed'] 
	
	country.active = state_data['active'] 
	
	country.deaths = state_data['deaths'] 
	
	country.recovered = state_data['recovered'] 

	db.add(country)
	db.commit()

@app.post("/state")
async def create_state(state_request: StateRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	"""
	Creates a new state and stores in database
	"""
	state = State()
	state.state = state_request.state
	
	db.add(state)
	db.commit()

	background_tasks.add_task(fetch_data, state.id)

	return {
		"code" : "success",
		"message" : "state created"
	}



#covid19 raw: https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv
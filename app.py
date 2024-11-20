from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Model for a candidate
class Candidate(BaseModel):
    id: int
    name: str
    party: str

# Model for a vote
class Vote(BaseModel):
    candidate_id: int
    voter_id: int  # In a real-world scenario, this would be tied to authenticated users

# Simulating databases
candidates_db = []
votes_db = []

# Route to register a candidate
@app.post("/api/register-candidate")
def register_candidate(candidate: Candidate):
    # Simulate saving the candidate (in reality, save to a database)
    candidates_db.append(candidate)
    return {"message": f"Candidate {candidate.name} registered successfully!"}

# Route to get all candidates
@app.get("/api/candidates", response_model=List[Candidate])
def get_candidates():
    if not candidates_db:
        raise HTTPException(status_code=404, detail="No candidates found")
    return candidates_db

# Route to submit a vote
@app.post("/api/vote")
def vote(vote: Vote):
    # Check if the candidate exists
    candidate = next((c for c in candidates_db if c.id == vote.candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Simulate saving the vote
    votes_db.append(vote)
    return {"message": "Vote submitted successfully!"}

# Route to get election results
@app.get("/api/results", response_model=List[dict])
def get_results():
    if not votes_db:
        raise HTTPException(status_code=404, detail="No votes found")
    
    # Tally votes for each candidate
    results = {}
    for vote in votes_db:
        candidate = next((c for c in candidates_db if c.id == vote.candidate_id), None)
        if candidate:
            if candidate.name in results:
                results[candidate.name] += 1
            else:
                results[candidate.name] = 1
    
    return [{"candidate": name, "votes": votes} for name, votes in results.items()]

# Root route with a welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Election Microservice!"}

# Run the app using uvicorn (this can be done directly or using the command line)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

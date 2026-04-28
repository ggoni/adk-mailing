import json
import asyncio
from sqlalchemy import text
from app.db.database import SessionLocal
from app.agents.copywriter import get_copywriter_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

class OrchestratorService:
    def __init__(self):
        self.agent = get_copywriter_agent()
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.agent,
            app_name="adk_mailing",
            session_service=self.session_service
        )

    async def run_orchestration(self):
        db = SessionLocal()
        try:
            # Fetch clusters excluding noise (-1)
            query = text("SELECT id, centroid_features FROM clusters_summary WHERE id != -1 AND centroid_features IS NOT NULL")
            clusters = db.execute(query).fetchall()
            
            count = 0
            for row in clusters:
                c_id = row[0]
                features = row[1]
                
                # Prepare JSON string
                if isinstance(features, str):
                    message_text = features
                else:
                    message_text = json.dumps(features)
                    
                session_id = f"cluster_{c_id}"
                
                # Create session (catch error if exists)
                try:
                    await self.session_service.create_session(app_name="adk_mailing", user_id="system", session_id=session_id)
                except Exception:
                    pass
                
                # Call agent via Runner
                user_message = Content(parts=[Part(text=message_text)])
                final_copy = ""
                
                for event in self.runner.run(user_id="system", session_id=session_id, new_message=user_message):
                    if event.is_final_response():
                        pass
                
                # Retrieve from state
                session = await self.session_service.get_session(app_name="adk_mailing", user_id="system", session_id=session_id)
                if "campaign_copy" in session.state:
                    final_copy = session.state["campaign_copy"]
                else:
                    final_copy = "Error: LLM output could not be retrieved from state."
                
                # Update Database
                exists = db.execute(text("SELECT id FROM campaign_copy WHERE cluster_id = :cid"), {"cid": c_id}).fetchone()
                if exists:
                    db.execute(
                        text("UPDATE campaign_copy SET generated_text = :txt WHERE cluster_id = :cid"), 
                        {"txt": final_copy, "cid": c_id}
                    )
                else:
                    db.execute(
                        text("INSERT INTO campaign_copy (cluster_id, generated_text) VALUES (:cid, :txt)"), 
                        {"cid": c_id, "txt": final_copy}
                    )
                
                count += 1
            
            db.commit()
            return count
        except Exception as e:
            db.rollback()
            print(f"Orchestration Error: {e}")
            raise
        finally:
            db.close()

if __name__ == "__main__":
    service = OrchestratorService()
    asyncio.run(service.run_orchestration())

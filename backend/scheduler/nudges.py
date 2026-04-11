from apscheduler.schedulers.blocking import BlockingScheduler
from agent.agent import run_agent
from db.sqlite_store import get_conn
import logging

logging.basicConfig(level=logging.INFO)
scheduler = BlockingScheduler()

def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id FROM users").fetchall()
    conn.close()
    return [r["id"] for r in rows]

@scheduler.scheduled_job("cron", day_of_week="mon", hour=9)
def weekly_nudge():
    users = get_all_users()
    logging.info(f"Running weekly nudge for {len(users)} users")
    for user_id in users:
        try:
            nudge = run_agent(
                user_id=user_id,
                user_message="Give me a quick weekly financial summary and one specific tip to improve my spending this week.",
            )
            # Log the nudge (could be sent via email/SMS in a real app)
            logging.info(f"[NUDGE SENT TO {user_id}]: {nudge}")
        except Exception as e:
            logging.error(f"Nudge failed for {user_id}: {e}")

if __name__ == "__main__":
    logging.info("Starting scheduler...")
    scheduler.start()

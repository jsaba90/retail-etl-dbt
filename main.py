from fastapi import FastAPI, HTTPException
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="DBT Runner API")

@app.get("/")
def read_root():
    return {"message": "DBT Runner API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/run")
def run_dbt():
    logger.info("Running dbt run command")

    # Run the dbt run command and capture the output
    result = subprocess.run(["dbt", "run"], capture_output=True, text=True)

    # Check the return code of the command
    if result.returncode == 0:
        # The command succeeded
        logger.info("dbt run command succeeded")
        logger.info("dbt run output: " + result.stdout)
        logger.info("dbt run error: " + result.stderr)
        return {"output": result.stdout, "error": result.stderr}
    else:
        # The command failed
        error_message = f"dbt run command failed with error: {result.stderr} stdout: {result.stdout}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


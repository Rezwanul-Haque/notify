### Local Development:

- Create a `.env` file in project root directory (see `.env.example` for sample)

- Create a virtual environment.

- Open Terminal (from project directory). After activating virtual environment, terminal will look something like this:

    `(.venv) user@<pc_name>:~/<path_to_work_directory>/pi-notify$`
    
- Install requirements
    - `pip install -r requirements.txt`

## Run
```
python -m uvicorn app.main:app --reload
```
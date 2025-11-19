import subprocess

def run(name):
    print(f"Running {name}...")
    subprocess.run(["python", name], check=True)

if __name__ == "__main__":
    run("ingest.py")
    run("transform.py")
    run("publish.py")
    print("Pipeline completed successfully!")

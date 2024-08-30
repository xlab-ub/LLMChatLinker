# llmchatlinker/main.py

from .orchestrator import Orchestrator

def main():
    orchestrator = Orchestrator()
    orchestrator.start()

if __name__ == "__main__":
    main()
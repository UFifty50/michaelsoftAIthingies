from typing import Dict, List

# internal imports
from Models.Generators import DataExtractorGPT, CalculationsGPT, AnalysisReportGPT, FinalReportGPT
from Doc import CsvDoc


import openai
openai.api_key = "62437466-c110-4947-a0bb-0c38c870cc95"
openai.api_base = "https://polite-ground-030dc3103.4.azurestaticapps.net/api/v1"
openai.api_type = "azure"
openai.api_version = "2023-05-15"
deployment_name = "gpt-35-hackathon"

dataExtractor = DataExtractorGPT.DataExtractor()
calculationGen = CalculationsGPT.Calculations()
analysisReportGen = AnalysisReportGPT.AnalysisReport()
finalReportGen = FinalReportGPT.FinalReport()


def main(argv: list[str]) -> int:
    # TODO: take docs and prompt from UI or API
    # TODO: convert all non-text files to CSV
    docArr: List[str] = argv[1:argv.index(':')]
    prompt: str = " ".join(argv[argv.index(':')+1:])
    
    docFileArr: List[CsvDoc] = [CsvDoc(docArr[docArr.index(doc)], open(doc)) for doc in docArr]
    
    dataNeededPrompt: str = dataExtractor.concat(prompt, docFileArr)
    dataNeeded: str = dataExtractor.send(dataNeededPrompt)
    
    calculationsNeededPrompt: str = calculationGen.concat(prompt, dataNeeded)
    calculationsNeeded: str = calculationGen.send(calculationsNeededPrompt)
    
    # TODO: do calculations
    calculationAns: Dict[str, str] = {"days": "167"}
    
    analysisReportPrompt: str = analysisReportGen.concat(prompt, calculationAns)
    analysisReport: str = analysisReportGen.send(analysisReportPrompt)
    
    # prep final prompt
    finalReportPrompt: str = finalReportGen.concat(prompt, dataNeeded, analysisReport)
    finalReport: str = finalReportGen.send(finalReportPrompt)
    
    print(finalReport)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))

# from fastapi.concurrency import asynccontextmanager
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import FastAPI
# from .routers import users


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("Startup")
#     try:
#         yield
#     finally:
#         print("Shutdown")

# app: FastAPI = FastAPI(lifespan=lifespan)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# app.include_router(users.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# class Generator: 
#     messageBlock: list[str]

# @app.post("/api/v1/generator")
# def feed_generator(generator: Generator):
#     return {"message": "Generator received"}

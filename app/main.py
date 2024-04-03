from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Dict, List, Set
import defusedxml
import uvicorn

defusedxml.defuse_stdlib()

# internal imports
from Models.Generators import (
    DataExtractorGPT,
    CalculationsGPT,
    AnalysisReportGPT,
    FinalReportGPT,
)  # noqa: E402
from Doc import CsvDoc  # noqa: E402


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


class PromptRequest(BaseModel):
    prompt: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup")
    try:
        yield
    finally:
        print("Shutdown")


def main(argv: list[str]) -> int:
    # TODO: take docs and prompt from UI or API
    # TODO: convert all non-text files to CSV
    docArr: List[str] = argv[1 : argv.index(":")]
    prompt: str = " ".join(argv[argv.index(":") + 1 :])

    docFileArr: List[CsvDoc] = [
        CsvDoc(docArr[docArr.index(doc)], open(doc, "rb")) for doc in docArr
    ]

    dataNeededPrompt: str = dataExtractor.concat(prompt, docFileArr)
    dataNeeded: str = dataExtractor.send(dataNeededPrompt)

    calculationsNeededPrompt: str = calculationGen.concat(prompt, dataNeeded)
    calculationsNeeded: str = calculationGen.send(calculationsNeededPrompt)
    print(calculationsNeeded, "\n\n\n\n")

    # TODO: do calculations
    calculationAns: Dict[str, str] = {}  # {"days": "167"}

    analysisReportPrompt: str = analysisReportGen.concat(
        prompt, docFileArr, dataNeeded, calculationAns
    )
    analysisReport: str = analysisReportGen.send(analysisReportPrompt)

    # prep final prompt
    finalReportPrompt: str = finalReportGen.concat(
        prompt, docFileArr, dataNeeded, analysisReport
    )
    finalReport: str = finalReportGen.send(finalReportPrompt)

    print(analysisReportPrompt, "\n\n", finalReport)

    return 0


if __name__ == "__main__":
    # import sys
    # sys.exit(main(sys.argv))
    app: FastAPI = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=999,
    )

    fileStore: Set[CsvDoc] = set()

    # redirect to nodejs frontend
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.post("/api/v1/prompt")
    async def prompt(prompt: PromptRequest):
        # pass the prompt through the analysis pipeline with the docs
        dataNeededPrompt: str = dataExtractor.concat(prompt.prompt, fileStore)
        dataNeeded: str = dataExtractor.send(dataNeededPrompt)

        calculationsNeededPrompt: str = calculationGen.concat(prompt.prompt, dataNeeded)
        calculationsNeeded: str = calculationGen.send(calculationsNeededPrompt)
        print(calculationsNeeded, "\n\n\n\n")

        # TODO: do calculations
        calculationAns: Dict[str, str] = {}  # {"days": "167"}

        analysisReportPrompt: str = analysisReportGen.concat(
            prompt.prompt, fileStore, dataNeeded, calculationAns
        )
        analysisReport: str = analysisReportGen.send(analysisReportPrompt)

        # prep final prompt
        finalReportPrompt: str = finalReportGen.concat(
            prompt.prompt, fileStore, dataNeeded, analysisReport
        )
        finalReport: str = finalReportGen.send(finalReportPrompt)

        return {"final": finalReport}

    @app.post("/api/v1/upload")
    async def uploadFile(files: List[UploadFile] = File(...)):
        if len(files) == 0:
            return {"error": "No files uploaded"}

        for idx, file in enumerate(files):
            if file.filename is None:
                return {"error": f"No filename provided for file {idx}"}
            fileStore.add(CsvDoc(file.filename, await file.read()))

        return {"filenames": [file.filename for file in files]}

    @app.get("/viewFiles")
    async def viewFiles():
        return {"files": fileStore}

    uvicorn.run(app)

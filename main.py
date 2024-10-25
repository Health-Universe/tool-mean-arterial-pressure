"""FastAPI application for calculating Mean Arterial Pressure (MAP)."""
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Mean Arterial Pressure (MAP) Tool",
    description="API for calculating Mean Arterial Pressure based on Systolic and Diastolic Blood Pressure.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MAPFormInput(BaseModel):
    """Form-based input schema for calculating Mean Arterial Pressure (MAP)."""

    systolic_bp: int = Field(
        title="Systolic Blood Pressure (SBP)",
        ge=50,
        le=250,
        examples=[120],
        description="Enter your systolic blood pressure (SBP) in mmHg. Must be between 50 and 250.",
    )
    diastolic_bp: int = Field(
        title="Diastolic Blood Pressure (DBP)",
        ge=30,
        le=150,
        examples=[80],
        description="Enter your diastolic blood pressure (DBP) in mmHg. Must be between 30 and 150.",
    )


class MAPFormOutput(BaseModel):
    """Form-based output schema for Mean Arterial Pressure (MAP)."""

    map: float = Field(
        title="Mean Arterial Pressure (MAP)",
        examples=[93.3],
        description="Your calculated Mean Arterial Pressure (MAP) in mmHg.",
    )


@app.post(
    "/calculate",
    description="Calculate Mean Arterial Pressure (MAP) based on Systolic and Diastolic Blood Pressure.",
    response_model=MAPFormOutput,
)
async def calculate_map(
    data: Annotated[MAPFormInput, Form()],
) -> MAPFormOutput:
    """Calculate Mean Arterial Pressure (MAP).

    Args:
        data (MAPFormInput): The input data containing systolic and diastolic blood pressure.

    Returns:
        MAPFormOutput: The calculated MAP.
    """
    # Calculate MAP using the formula: MAP = (SBP + 2*DBP) / 3
    map_value = (data.systolic_bp + 2 * data.diastolic_bp) / 3

    # Optionally, round the result to one decimal place
    map_value = round(map_value, 1)

    return MAPFormOutput(map=map_value)

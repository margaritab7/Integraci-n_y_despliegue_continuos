import json
from typing import Any

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
<<<<<<< HEAD
#from model import __version__ as "0.0.1"
#from model.predict import make_prediction
# Comentamos la importación del modelo y de make_prediction
sed -i 's/^from model\.predict import make_prediction/# from model.predict import make_prediction/' app/api.py
sed -i 's/^from model import __version__ as "0.0.1"/# from model import __version__ as "0.0.1"/' app/api.py
=======
try:
    from model import __version__ as model_version
    from model.predict import make_prediction
except Exception:  # Fallback if packaged model isn't available
    model_version = "0.0.1"

    def make_prediction(input_data):
        try:
            n = len(input_data) if hasattr(input_data, "__len__") else 1
        except Exception:
            n = 1
        return {"predictions": [0] * n, "errors": None, "version": model_version}
>>>>>>> 36df1cfb696febaefd4e385f7976d0a96f141531

# Cambiamos cualquier uso de "0.0.1" por un literal
sed -i 's/"0.0.1"/"0.0.1"/g' app/api.pycat >> app/api.py << 'EOF'

# --- Stub temporal cuando no está instalado el paquete del modelo ---
def make_prediction(input_data):
    # Devuelve una predicción de ejemplo y sin errores
    try:
        n = len(input_data) if hasattr(input_data, "__len__") else 1
    except Exception:
        n = 1
    return {"predictions": [0]*n, "errors": None, "version": "0.0.1"}
# --- Fin stub temporal ---
EOF
from app import __version__, schemas
from app.config import settings

api_router = APIRouter()

# Ruta para verificar que la API se esté ejecutando correctamente
@api_router.get("/health", response_model=schemas.Health, status_code=200)
def health() -> dict:
    """
    Root Get
    """
    health = schemas.Health(
        name=settings.PROJECT_NAME, api_version=__version__, "0.0.1"="0.0.1"
    )

    return health.dict()

# Ruta para realizar las predicciones
@api_router.post("/predict", response_model=schemas.PredictionResults, status_code=200)
async def predict(input_data: schemas.MultipleDataInputs) -> Any:
    """
    Prediccion usando el modelo de bankchurn
    """

    input_df = pd.DataFrame(jsonable_encoder(input_data.inputs))

    logger.info(f"Making prediction on inputs: {input_data.inputs}")
    results = make_prediction(input_data=input_df.replace({np.nan: None}))

    if results["errors"] is not None:
        logger.warning(f"Prediction validation error: {results.get('errors')}")
        raise HTTPException(status_code=400, detail=json.loads(results["errors"]))

    logger.info(f"Prediction results: {results.get('predictions')}")

    return results

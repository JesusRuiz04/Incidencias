"""
Análisis avanzado de reportes usando pandas.
"""

import pandas as pd
from datetime import datetime, timedelta
from src.models import SessionLocal, Incidencia


def obtener_reportes_por_periodo(usuario_id: int, periodo: str = "semanal"):
    """
    Analiza reportes agrupados por período (semanal o mensual).
    
    Args:
        usuario_id: ID del usuario
        periodo: "semanal" o "mensual"
    
    Returns:
        Dict con análisis de reportes por período
    """
    db = SessionLocal()
    
    try:
        # Obtener reportes del usuario
        reportes = db.query(Incidencia).filter(
            Incidencia.usuario_id == usuario_id
        ).all()
        
        if not reportes:
            return {
                "periodo": periodo,
                "total_reportes": 0,
                "por_periodo": [],
                "promedio_por_periodo": 0,
                "estado_por_periodo": [],
                "tipo_mas_comun": None
            }
        
        # Convertir a DataFrame
        datos = [
            {
                'id': r.id,
                'titulo': r.titulo,
                'tipo': r.tipo,
                'estado': r.estado,
                'prioridad': r.prioridad,
                'fecha': r.fecha_creacion,
            }
            for r in reportes
        ]
        
        df = pd.DataFrame(datos)
        df['fecha'] = pd.to_datetime(df['fecha'])
        
        # Agrupar por período
        if periodo == "semanal":
            df['periodo'] = df['fecha'].dt.strftime('%Y-W%U')  # Año-Semana
            label_periodo = "Semana"
        else:  # mensual
            df['periodo'] = df['fecha'].dt.strftime('%Y-%m')  # Año-Mes
            label_periodo = "Mes"
        
        # Contar reportes por período
        por_periodo = df.groupby('periodo').size().to_dict()
        
        # Estadísticas por período
        estado_por_periodo = df.groupby(['periodo', 'estado']).size().unstack(fill_value=0).to_dict('index')
        
        # Tipo más común
        tipo_mas_comun = df['tipo'].value_counts().idxmax() if len(df) > 0 else None
        
        # Prioridad más reportada
        prioridad_mas_comun = df['prioridad'].value_counts().idxmax() if len(df) > 0 else None
        
        # Promedio de reportes por período
        promedio = len(reportes) / len(por_periodo) if por_periodo else 0
        
        # Formatear resultado
        por_periodo_formateado = [
            {
                "periodo": periodo_key,
                "total": int(count),
                "estados": {
                    "abierto": int(estado_por_periodo.get(periodo_key, {}).get('abierto', 0)),
                    "en_progreso": int(estado_por_periodo.get(periodo_key, {}).get('en_progreso', 0)),
                    "cerrado": int(estado_por_periodo.get(periodo_key, {}).get('cerrado', 0)),
                }
            }
            for periodo_key, count in sorted(por_periodo.items())
        ]
        
        return {
            "periodo": periodo,
            "total_reportes": len(reportes),
            "por_periodo": por_periodo_formateado,
            "promedio_por_periodo": round(promedio, 2),
            "tipo_mas_comun": tipo_mas_comun,
            "prioridad_mas_comun": prioridad_mas_comun,
            "label_periodo": label_periodo
        }
        
    finally:
        db.close()


def obtener_tendencias(usuario_id: int, dias: int = 30):
    """
    Analiza tendencias de reportes en los últimos N días.
    
    Args:
        usuario_id: ID del usuario
        dias: Número de días a analizar
    
    Returns:
        Dict con tendencias
    """
    db = SessionLocal()
    
    try:
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        reportes = db.query(Incidencia).filter(
            Incidencia.usuario_id == usuario_id,
            Incidencia.fecha_creacion >= fecha_inicio
        ).all()
        
        if not reportes:
            return {
                "dias": dias,
                "total_reportes": 0,
                "por_dia": [],
                "velocidad_resolucion": None
            }
        
        datos = [
            {
                'fecha': r.fecha_creacion,
                'estado': r.estado,
                'tipo': r.tipo,
            }
            for r in reportes
        ]
        
        df = pd.DataFrame(datos)
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date
        
        # Reportes por día
        por_dia = df.groupby('fecha').size().to_dict()
        
        # Tasa de resolución (cerrados vs total)
        total = len(df)
        cerrados = len(df[df['estado'] == 'cerrado'])
        velocidad_resolucion = round((cerrados / total * 100), 2) if total > 0 else 0
        
        # Formatear
        por_dia_formateado = [
            {
                "fecha": str(fecha),
                "total": count
            }
            for fecha, count in sorted(por_dia.items())
        ]
        
        return {
            "dias": dias,
            "total_reportes": total,
            "cerrados": cerrados,
            "por_dia": por_dia_formateado,
            "velocidad_resolucion_pct": velocidad_resolucion,
        }
        
    finally:
        db.close()


def exportar_reportes_csv(usuario_id: int, formato: str = "csv"):
    """
    Exporta reportes a DataFrame (para guardar como CSV/Excel).
    
    Args:
        usuario_id: ID del usuario
        formato: "csv" o "excel"
    
    Returns:
        DataFrame con los reportes
    """
    db = SessionLocal()
    
    try:
        reportes = db.query(Incidencia).filter(
            Incidencia.usuario_id == usuario_id
        ).all()
        
        if not reportes:
            return pd.DataFrame()
        
        datos = [
            {
                'ID': r.id,
                'Título': r.titulo,
                'Descripción': r.descripcion,
                'Ubicación': r.ubicacion,
                'Tipo': r.tipo,
                'Estado': r.estado,
                'Prioridad': r.prioridad,
                'Fecha Creación': r.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for r in reportes
        ]
        
        df = pd.DataFrame(datos)
        return df
        
    finally:
        db.close()

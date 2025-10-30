import streamlit as st
import pandas as pd
import plotly.express as px
# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Vehículos",
    page_icon="🚗",
    layout="wide"
)
# Título principal
st.title('🚗 Análisis de Vehículos en Venta')
st.markdown("---")
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('vehicles_us.csv')
        return df
    except FileNotFoundError:
        st.error("No se pudo encontrar el archivo vehicles_us.csv")
        return pd.DataFrame()
car_data = load_data()
# Mostrar datos si están disponibles
if not car_data.empty:
    st.sidebar.header("Filtros")
    # Filtros en sidebar
    selected_condition = st.sidebar.multiselect(
        'Condición del vehículo:',
        options=car_data['condition'].unique(),
        default=car_data['condition'].unique()
    )    
    min_year, max_year = st.sidebar.slider(
        'Año del modelo:',
        min_value=int(car_data['model_year'].min()),
        max_value=int(car_data['model_year'].max()),
        value=(int(car_data['model_year'].min()), int(car_data['model_year'].max()))
    )
    
    # Aplicar filtros
    filtered_data = car_data[
        (car_data['condition'].isin(selected_condition)) &
        (car_data['model_year'] >= min_year) &
        (car_data['model_year'] <= max_year)
    ]
    
    # Mostrar estadísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de vehículos", len(filtered_data))
    
    with col2:
        st.metric("Precio promedio", f"${filtered_data['price'].mean():,.0f}")
    
    with col3:
        st.metric("Año promedio", f"{filtered_data['model_year'].mean():.0f}")
    
    with col4:
        st.metric("Odómetro promedio", f"{filtered_data['odometer'].mean():,.0f} km")
    
    st.markdown("---")
    
    # Sección de gráficos
    st.header("📊 Visualizaciones")
    
    # Opción 1: Botones
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Usando Botones")
        
        hist_button = st.button('Construir Histograma de Precios')
        if hist_button:
            st.write('### Histograma de Distribución de Precios')
            fig_hist = px.histogram(
                filtered_data, 
                x='price',
                title='Distribución de Precios de Vehículos',
                labels={'price': 'Precio (USD)'},
                color_discrete_sequence=['#FF4B4B']
            )
            fig_hist.update_layout(
                xaxis_title="Precio (USD)",
                yaxis_title="Cantidad de Vehículos"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        scatter_button = st.button('Construir Gráfico de Dispersión')
        if scatter_button:
            st.write('### Precio vs Año del Modelo')
            fig_scatter = px.scatter(
                filtered_data,
                x='model_year',
                y='price',
                color='condition',
                title='Relación entre Precio y Año del Modelo',
                labels={'model_year': 'Año del Modelo', 'price': 'Precio (USD)'},
                hover_data=['model', 'odometer']
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Opción 2: Checkboxes (desafío extra)
    st.subheader("🎛️ Usando Casillas de Verificación")
    
    col1, col2 = st.columns(2)
    
    with col1:
        build_histogram = st.checkbox('Mostrar Histograma de Odómetro')
        if build_histogram:
            st.write('### Distribución del Odómetro')
            fig_odo_hist = px.histogram(
                filtered_data,
                x='odometer',
                title='Distribución del Odómetro',
                labels={'odometer': 'Odómetro (km)'},
                color_discrete_sequence=['#00D4AA']
            )
            st.plotly_chart(fig_odo_hist, use_container_width=True)
    
    with col2:
        build_scatter = st.checkbox('Mostrar Dispersión Precio vs Odómetro')
        if build_scatter:
            st.write('### Precio vs Odómetro')
            fig_odo_scatter = px.scatter(
                filtered_data,
                x='odometer',
                y='price',
                color='condition',
                title='Relación entre Precio y Odómetro',
                labels={'odometer': 'Odómetro (km)', 'price': 'Precio (USD)'},
                hover_data=['model_year', 'model']
            )
            st.plotly_chart(fig_odo_scatter, use_container_width=True)
    
    # Gráfico adicional: Boxplot por condición
    st.markdown("---")
    st.subheader("📦 Análisis por Condición")
    
    build_boxplot = st.checkbox('Mostrar Boxplot de Precios por Condición')
    if build_boxplot:
        fig_box = px.box(
            filtered_data,
            x='condition',
            y='price',
            title='Distribución de Precios por Condición del Vehículo',
            labels={'condition': 'Condición', 'price': 'Precio (USD)'},
            color='condition'
        )
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Mostrar datos filtrados
    st.markdown("---")
    st.subheader("📋 Datos Filtrados")
    
    if st.checkbox('Mostrar tabla de datos'):
        st.dataframe(filtered_data.head(100))
        
        # Opción para descargar datos filtrados
        csv = filtered_data.to_csv(index=False)
        st.download_button(
            label="📥 Descargar datos filtrados como CSV",
            data=csv,
            file_name='vehiculos_filtrados.csv',
            mime='text/csv'
        )

else:
    st.error("No se pudieron cargar los datos. Verifica que el archivo vehicles_us.csv esté en el directorio correcto.")

# Footer
st.markdown("---")
st.markdown(
    "**Dashboard creado con Streamlit** | "
    "Datos: vehicles_us.csv"
)
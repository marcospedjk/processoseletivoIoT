import machine
import time

# ==========================================
# Configuração de Parâmetros e Pinos
# ==========================================
LIMITE_TEMPO_X = 5000       # Tempo máximo de porta aberta em ms (5 segundos)
LIMITE_VARIACAO_Y = 3.0     # Gradiente máximo de temperatura em °C (Delta T)

# Botão na GPIO 4 (PULL_DOWN garante: 0 = Solto/Aberto, 1 = Pressionado/Fechado)
btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Configuração I2C para o sensor MPU6050 (SDA=21, SCL=22)
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Inicializa (acorda) o MPU6050
try:
    i2c.writeto_mem(0x68, 0x6B, b'\x00')
except:
    pass

def ler_temperatura():
    """Lê os registradores do MPU6050 e converte para °C"""
    try:
        raw = i2c.readfrom_mem(0x68, 0x41, 2)
        val = (raw[0] << 8) | raw[1]
        if val >= 0x8000:
            val -= 0x10000
        return (val / 340.0) + 36.53
    except:
        return 20.0  # Valor padrão seguro caso falhe a leitura inicial

# ==========================================
# Variáveis de Estado
# ==========================================
alert_door = False
alert_temp = False
door_is_open = False
door_open_start_time = 0

# Mensagem OBRIGATÓRIA de inicialização exigida pelo teste
print("Sistema de Monitoramento Inicializado")

# Temperatura inicial de referência
t_ref = ler_temperatura()

# ==========================================
# Loop Principal (Não-Bloqueante)
# ==========================================
while True:
    current_time = time.ticks_ms()
    door_state = btn.value()       # 1 = Fechada, 0 = Aberta
    t_atual = ler_temperatura()
    
    # 1. Monitoramento do Tempo de Porta Aberta
    if door_state == 0:  # Porta Aberta
        if not door_is_open:
            door_is_open = True
            door_open_start_time = current_time
        else:
            if time.ticks_diff(current_time, door_open_start_time) >= LIMITE_TEMPO_X:
                if not alert_door:
                    print("ALERTA: Porta aberta por muito tempo!")
                    alert_door = True
    else:  # Porta Fechada
        door_is_open = False
        if not alert_door and not alert_temp:
            t_ref = t_atual

    # 2. Monitoramento de Elevação Térmica
    delta_t = t_atual - t_ref
    if delta_t >= LIMITE_VARIACAO_Y:
        if not alert_temp:
            print("ALERTA: Degradacao termica detectada!")
            alert_temp = True

    # 3. Restauração do Estado (Normalização)
    if door_state == 1 and delta_t < LIMITE_VARIACAO_Y:
        if alert_door or alert_temp:
            print("Status: Sistema Normalizado.")
            alert_door = False
            alert_temp = False
            t_ref = t_atual
            
    time.sleep_ms(50)
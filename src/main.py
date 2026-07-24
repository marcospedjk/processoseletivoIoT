import machine
import time


# Configuração de Parâmetros e Pinos

LIMITE_TEMPO_X = 4800       # Margem para latência do CI
LIMITE_VARIACAO_Y = 3.0     # Delta T máximo em °C

# Botão na GPIO 4
btn = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Configuração I2C para o sensor MPU6050
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Inicializa MPU6050
try:
    i2c.writeto_mem(0x68, 0x6B, b'\x00')
except:
    pass

def ler_temperatura():
    """Lê a temperatura do MPU6050"""
    try:
        raw = i2c.readfrom_mem(0x68, 0x41, 2)
        val = (raw[0] << 8) | raw[1]
        if val >= 0x8000:
            val -= 0x10000
        return (val / 340.0) + 36.53
    except:
        return 20.0


# Variáveis de Estado

alert_door = False
alert_temp = False
door_is_open = False
door_open_start_time = 0

# Mensagem OBRIGATÓRIA de inicialização
print("Sistema de Monitoramento Inicializado")

t_ref = ler_temperatura()


# Loop Principal

while True:
    current_time = time.ticks_ms()
    door_state = btn.value()  # 0 = Aberta, 1 = Fechada
    t_atual = ler_temperatura()
    delta_t = t_atual - t_ref

    # --- 1. DETECÇÃO DE ABERTURA / FECHAMENTO DA PORTA ---
    if door_state == 0:  # Porta Aberta
        # Se a porta acabou de ser detectada como aberta, inicia o cronômetro
        if not door_is_open:
            door_is_open = True
            door_open_start_time = current_time
        
        # Se continuar aberta e estourar o limite de tempo
        if time.ticks_diff(current_time, door_open_start_time) >= LIMITE_TEMPO_X:
            if not alert_door:
                print("ALERTA: Porta aberta por muito tempo!")
                alert_door = True
    else:  # Porta Fechada
        door_is_open = False  # Reseta o controle de abertura

    # --- 2. MONITORAMENTO DE TEMPERATURA ---
    if delta_t >= LIMITE_VARIACAO_Y:
        if not alert_temp:
            print("ALERTA: Degradacao termica detectada!")
            alert_temp = True

    # --- 3. REQUISITO DE NORMALIZAÇÃO ---
    # Só normaliza quando a porta está fechada (1) AND a variação térmica está OK
    if door_state == 1 and delta_t < LIMITE_VARIACAO_Y:
        if alert_door or alert_temp:
            print("Status: Sistema Normalizado.")
            alert_door = False
            alert_temp = False
            t_ref = t_atual  # Atualiza a referência de temperatura

   
    time.sleep_ms(10)
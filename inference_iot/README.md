# Project presentatio at:
https://tome.app/cileb/insect-detection-iot-system-for-agriculture-clk8hfau306j3mq3cx666xhx2

# Attuazione su Arduino

L'arduino il cui micro_id risulta presente nella lista dei microcontrollori infestati gli viene inviato un pacchetto per far accendere il led che vi è attaccato, in modo da segnalare la presenza di un microcontrollore infestato.

Se il micro_id non è presente nella lista dei microcontrollori infestati, viene inviato un pacchetto per far spegnere il led che vi è attaccato, in modo da segnalare la presenza di un microcontrollore non infestato.

## Flow fra bridge e arduino

Nel loop del bridge :

### Attuazione
			
        # funzione in utils che se ritorna a true si invia un pacchetto seriale al microcontrollore per accendere il led
        mic_state = checkInfectedMicrocontrollers() #assegno vero se la varibile è presente nella lista 
        set_micro_light(mic_state, self.ser) #accendo il led se mic_state è True
            
        #poi si fa la lettura del seriale per vedere le foto ricevute
        #look for a byte from serial
        if not self.ser is None:


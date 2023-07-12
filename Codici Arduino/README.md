MOTION DETECTION WITH PIR SENSOR

Il loop del codice è diviso in due parti.

Nella prima parte, viene eseguita una verifica sulla durata trascorsa da quando è stato attivato l'ultimo intervallo seriale. Se la durata è maggiore o uguale all'intervallo seriale, viene stampato un messaggio sulla seriale indicando che il sensore è attivo e viene aggiornato il valore di lastMillis all'istante corrente.

In pratica, questo blocco di codice sta garantendo che il sensore PIR venga letto solo ogni SERIAL_INTERVAL millisecondi, evitando di eseguire letture troppo frequenti eccessivamente costose in termini di risorse di sistema.

Nella seconda parte, viene controllato lo stato di fS (flag State). Se fS è uguale a 0, viene letto il valore del sensore PIR (movimento). Se il valore è HIGH, viene stampato un messaggio sulla seriale indicando il rilevamento del movimento, viene accesa la luce LED e il valore di fS viene impostato a 1.

Se invece fS è uguale a 1, viene calcolato il tempo trascorso dall'ultimo cambiamento di stato e confrontato con il valore di debounce time. Se il tempo trascorso è maggiore o uguale al debounce time, viene spenta la luce LED, inviati tre byte sulla seriale e il valore di fS viene impostato a 0.

In questo modo il codice esegue in modo efficiente il controllo del sensore PIR, mantenendo un intervallo costante di stampa sulla seriale, senza utilizzare la funzione delay().
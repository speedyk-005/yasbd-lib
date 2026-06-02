ISO_CODE = "es"
TEST_DATA = [
    # Basic punctuation
    "Hola mundo.| ¿Cómo estás?| Bien, gracias.",
    "¿Cuál es tu nombre?| Me llamo Carlos.",
    # Abbreviations (Titles & Social)
    "El Sr. García llegó ayer.| La Sra. López también.",
    "La Profe. María dio una conferencia.",
    "El Lcdo. Pérez y el Mag. Torres son amigos.",
    "D. José y Dña. María son los dueños.",
    "El Cmdte. Rodríguez saludó al Cnel. Díaz.",
    # Abbreviations (References & Documents)
    "Véase la pág. 55 del libro.",
    "Vea el cap. 3 en el t. II de la obra.",
    "El art. 4 y el nro. 8 son clave.",
    "Llama al dir. general al tel. 555-1234.",
    "Compré pan, leche, etc. para la cena.",
    "Lea p. ej. el capítulo 5.",
    "La reunión es el lun. 15 de enero.",
    "Nació el 5 de abr. de 1990.",
    # Addresses & Locations
    "Vive en la Av. Siempre Viva.",
    "Viven en la C. Mayor, 12.",
    "El accidente fue en la Cra. 50 con Cll. 100.",
    "Dobla en la Transv. 3 y sigue por la Diag. 5.",
    "La casa está en la Urb. Las Rosas, Mz. A, Lt. 15 del Asent. Humano.",
    # Geopolitical & Organizations
    "El presidente de los EE.UU. visitó Europa.",
    "Las FF.AA. emitieron un comunicado oficial.",
    "El departamento de RR.HH. aprobó las vacaciones.",
    "Es una de las CC.AA. más grandes de España.",
    "El EE.UU. Gobierno aprobó la ley.",
    "Las FF.AA. Ministerio anunciaron cambios.",
    "El RR.HH. Instituto cerró hoy.",
    # Common Starters after abbreviations
    "Llegó el Sr. Por suerte trajo el paquete.",
    "Fui a la Cra. Para ver el desfile.",
    "Llegó el Sr. García.| Como no estaba, se fue.",
    # Pronoun heuristic (Ud./Vd.)
    "Me dirijo a Ud. Marco, para saludarlo.",
    "Me dirijo a Ud.| Mañana le enviaré el paquete.",
    "Se lo di a Uds.| Ellos lo confirmaron.",
    "Hablé con Ud.| Afortunadamente todo se resolvió.",
    "Le escribí a Ud.| Sin embargo, no respondió.",
    "Pregunté por Vds.| Lamentablemente no estaban.",
    "Me dirijo a Ud.| ¿Cuándo me enviará el paquete?",
    # Dates
    "La reunión es el lun. 15 de enero.",
    "Él dijo (No estoy listo.) durante la reunión.",
    "Él preguntó: ¿Estás listo?| Respondí que sí.",
    'Ella dijo: "No estoy segura."| Luego se fue.',
    # Ellipsis
    "El proyecto estaba casi terminado... pero encontramos un problema.",
    # Multiple sentences with various punctuation
    "¡Qué día tan maravilloso!| El sol brilla, los pájaros cantan...| Es un día perfecto para un picnic.",
    "¿Viste la película anoche?.| Sí, fue increíble.| ¡Me encantó!| La actuación fue excelente, aunque el final fue un poco predecible.",
]

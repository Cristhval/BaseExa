document.addEventListener('DOMContentLoaded', () => {
  const preguntasContainer = document.getElementById('preguntas-container');
  const addPreguntaBtn = document.getElementById('add-pregunta');

  // Templates ocultos
  const preguntaTemplate = document.getElementById('pregunta-template').innerHTML.trim();
  const respuestaTemplate = document.getElementById('respuesta-template').innerHTML.trim();

  // Función para actualizar los índices en los atributos name, id y for
  function actualizarIndices(element, tipo, nuevoIndice) {
    const regex = new RegExp(`(${tipo}-)(\\d+)`, 'g');
    const regexPrefix = new RegExp('__prefix__', 'g');

    // Actualizar name, id y for en todos los inputs y labels dentro de element
    element.querySelectorAll('*').forEach(el => {
      if (el.hasAttribute('name'))
        el.name = el.name.replace(regexPrefix, nuevoIndice).replace(regex, `$1${nuevoIndice}`);

      if (el.hasAttribute('id'))
        el.id = el.id.replace(regexPrefix, nuevoIndice).replace(regex, `$1${nuevoIndice}`);

      if (el.hasAttribute('for'))
        el.htmlFor = el.htmlFor.replace(regexPrefix, nuevoIndice).replace(regex, `$1${nuevoIndice}`);
    });
  }

  // Función para actualizar TOTAL_FORMS en management forms
  function actualizarTotalForms(prefix, nuevoTotal) {
    const totalFormsInput = document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
    if (totalFormsInput) totalFormsInput.value = nuevoTotal;
  }

  // Contador de preguntas (basado en management form)
  const totalPreguntasInput = document.querySelector('input[name="pregunta_set-TOTAL_FORMS"]');
  let totalPreguntas = totalPreguntasInput ? parseInt(totalPreguntasInput.value) : 0;

  // Añadir nueva pregunta
  addPreguntaBtn.addEventListener('click', () => {
    // Crear nuevo bloque pregunta desde template
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = preguntaTemplate;
    const nuevaPregunta = tempDiv.firstElementChild;

    // Actualizar índices pregunta
    actualizarIndices(nuevaPregunta, 'pregunta_set', totalPreguntas);

    // Dentro de esta pregunta, actualizar respuestas (vacío por ahora)
    // Actualizar management form respuestas: set TOTAL_FORMS a 1 (ya que se copia con 1 respuesta)
    actualizarTotalForms(`respuesta_set_${totalPreguntas}`, 1);

    // Añadir manejador para botón agregar respuesta dentro de la pregunta
    const addRespBtn = nuevaPregunta.querySelector('.add-respuesta');
    const respuestasContainer = nuevaPregunta.querySelector('.respuestas-container');
    let totalRespuestas = 1; // por el template viene 1 respuesta

    addRespBtn.addEventListener('click', () => {
      const tempRespDiv = document.createElement('div');
      tempRespDiv.innerHTML = respuestaTemplate;
      const nuevaRespuesta = tempRespDiv.firstElementChild;

      // Actualizar índices respuesta (prefix es respuesta_set_{preguntaIndex})
      actualizarIndices(nuevaRespuesta, `respuesta_set_${totalPreguntas}`, totalRespuestas);

      respuestasContainer.appendChild(nuevaRespuesta);

      totalRespuestas++;
      actualizarTotalForms(`respuesta_set_${totalPreguntas}`, totalRespuestas);

      // Añadir evento para botón eliminar respuesta
      nuevaRespuesta.querySelector('.remove-btn').addEventListener('click', (e) => {
        e.target.closest('.respuesta-bloque').remove();
        totalRespuestas--;
        actualizarTotalForms(`respuesta_set_${totalPreguntas}`, totalRespuestas);
      });
    });

    // Añadir evento para botón eliminar pregunta
    nuevaPregunta.querySelector('.remove-btn').addEventListener('click', (e) => {
      e.target.closest('.pregunta-bloque').remove();
      totalPreguntas--;
      actualizarTotalForms('pregunta_set', totalPreguntas);
      // Aquí idealmente actualizar índices de preguntas y respuestas restantes,
      // pero es complejo, se puede manejar con un refresh o advertencia
    });

    preguntasContainer.appendChild(nuevaPregunta);

    totalPreguntas++;
    actualizarTotalForms('pregunta_set', totalPreguntas);
  });

  // Añadir eventos a botones "Agregar respuesta" y "Eliminar" en preguntas ya existentes
  document.querySelectorAll('.pregunta-bloque').forEach((preguntaBloque, preguntaIdx) => {
    const addRespBtn = preguntaBloque.querySelector('.add-respuesta');
    const respuestasContainer = preguntaBloque.querySelector('.respuestas-container');

    // Contar respuestas iniciales
    let totalRespuestas = respuestasContainer.querySelectorAll('.respuesta-bloque').length;

    // Evento para agregar respuesta
    addRespBtn.addEventListener('click', () => {
      const tempRespDiv = document.createElement('div');
      tempRespDiv.innerHTML = respuestaTemplate;
      const nuevaRespuesta = tempRespDiv.firstElementChild;

      actualizarIndices(nuevaRespuesta, `respuesta_set_${preguntaIdx}`, totalRespuestas);

      respuestasContainer.appendChild(nuevaRespuesta);

      totalRespuestas++;
      actualizarTotalForms(`respuesta_set_${preguntaIdx}`, totalRespuestas);

      nuevaRespuesta.querySelector('.remove-btn').addEventListener('click', (e) => {
        e.target.closest('.respuesta-bloque').remove();
        totalRespuestas--;
        actualizarTotalForms(`respuesta_set_${preguntaIdx}`, totalRespuestas);
      });
    });

    // Eventos para eliminar respuestas existentes
    respuestasContainer.querySelectorAll('.respuesta-bloque .remove-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.target.closest('.respuesta-bloque').remove();
        totalRespuestas--;
        actualizarTotalForms(`respuesta_set_${preguntaIdx}`, totalRespuestas);
      });
    });

    // Evento eliminar pregunta
    preguntaBloque.querySelector('.remove-btn').addEventListener('click', (e) => {
      e.target.closest('.pregunta-bloque').remove();
      totalPreguntas--;
      actualizarTotalForms('pregunta_set', totalPreguntas);
    });
  });
});
document.addEventListener('DOMContentLoaded', function () {
    const preguntaContainer = document.getElementById('preguntas-container');
    const addPreguntaBtn = document.getElementById('add-pregunta');

    let totalForms = document.querySelector('#id_pregunta-TOTAL_FORMS');
    let preguntaIndex = parseInt(totalForms.value);

    addPreguntaBtn.addEventListener('click', () => {
        const templateDiv = document.createElement('div');
        templateDiv.innerHTML = document.querySelector('#pregunta-template').innerHTML.replace(/__prefix__/g, preguntaIndex);
        const newPregunta = templateDiv.firstElementChild;

        // Añadir formulario de respuestas
        const respuestaContainer = newPregunta.querySelector('.respuestas-container');
        for (let i = 0; i < 4; i++) {
            const rTemplate = document.createElement('div');
            rTemplate.innerHTML = document.querySelector('#respuesta-template').innerHTML.replace(/__prefix__/g, i);
            respuestaContainer.appendChild(rTemplate.firstElementChild);
        }

        // Añadir botón eliminar
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'remove-btn';
        removeBtn.innerHTML = '&times;';
        removeBtn.onclick = function () {
            newPregunta.remove();
        };
        newPregunta.insertBefore(removeBtn, newPregunta.firstChild);

        preguntaContainer.appendChild(newPregunta);
        preguntaIndex++;
        totalForms.value = preguntaIndex;
    });
});

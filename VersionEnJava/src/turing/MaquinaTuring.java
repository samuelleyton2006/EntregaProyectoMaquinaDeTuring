package turing;

import java.util.ArrayList;
import java.util.List;

public class MaquinaTuring {
	private String cinta;
	private int posicionCabeza;
	private String estado;
	private final List<Transicion> transiciones;
	private final char simboloBlanco;

	public MaquinaTuring(String entrada, char simboloBlanco, List<Transicion> transiciones) {
		this.cinta = entrada + simboloBlanco; // Agregamos un espacio en blanco al final de la cinta
		this.posicionCabeza = 0;
		this.estado = "q0"; // Estado inicial.
		this.transiciones = transiciones;
		this.simboloBlanco = simboloBlanco;
	}

	public void ejecutar() {
		while (!estado.equals("accept") && !estado.equals("reject")) {
			// Imprime el estado actual y el contenido de la cinta
			imprimirEstadoActual();

			char simboloActual = cinta.charAt(posicionCabeza);
			Transicion transicion = encontrarTransicion(estado, simboloActual);

			// Si la transicion llega null, se definira por defecto el estado en null
			if (transicion == null) {
				estado = "reject";
				imprimirEstadoActual();
				return;
			}

			// Actualizamos la cinta con el símbolo a escribir.
			cinta = cinta.substring(0, posicionCabeza) + transicion.simboloParaEscribir
					+ cinta.substring(posicionCabeza + 1);

			// Movemos la cabeza de la cinta en la dirección indicada.
			// posicionCabeza = posicionCabeza + transicion.direccion (es lo mismo)

			// posicionCabeza = 5 +1 = 6
			// posicionCabeza = 5 -1 = 4
			posicionCabeza += transicion.direccion;

			// Se asegurara que la cabeza no se mueva fuera de los límites establecidos de
			// la cinta.
			if (posicionCabeza < 0) {
				cinta = simboloBlanco + cinta;
				posicionCabeza = 0;
			} else if (posicionCabeza >= cinta.length()) {
				cinta = cinta + simboloBlanco;
			}

			// Modificamos al siguiente estado.
			estado = transicion.siguienteEstado;
		}

		// Imprime el estado actual.
		imprimirEstadoActual();
		// Se valida si el estado es aceptado o rechazada
		if (estado.equals("accept")) {
			System.out.println("La cadena es aceptada.");
		} else {
			System.out.println("La cadena es rechazada.");
		}
	}

	private void imprimirEstadoActual() {
		// Imprimimos en consola la cinta con la posición de la cabeza.
		StringBuilder cintaConCabeza = new StringBuilder(cinta);
		cintaConCabeza.insert(posicionCabeza, '|');
		if (posicionCabeza < cinta.length() - 1) {
			cintaConCabeza.append('|');
		}
		System.out.println("Estado: " + estado);
		System.out.println("Cinta: " + cintaConCabeza.toString());
		System.out.println("Posición de la cabeza: " + posicionCabeza);
		System.out.println("------------------------------");
	}

	// Metodo que permite encontrar la posicion en la maquina de turing, si no se
	// encuentra se retorna en null
	private Transicion encontrarTransicion(String currentState, char readSymbol) {
		for (Transicion transicion : transiciones) {
			if (transicion.estadoActual.equals(currentState) && transicion.leerSimbolo == readSymbol) {
				return transicion;
			}
		}
		return null;
	}

	public static class Transicion {
		String estadoActual;
		char leerSimbolo;
		char simboloParaEscribir;
		int direccion;
		String siguienteEstado;

		public Transicion(String estadoActual, char leerSimbolo, char simboloParaEscribir, int direccion,
				String siguienteEstado) {
			this.estadoActual = estadoActual;
			this.leerSimbolo = leerSimbolo;
			this.simboloParaEscribir = simboloParaEscribir;
			this.direccion = direccion;
			this.siguienteEstado = siguienteEstado;
		}
	}

	// Metodo main
	public static void main(String[] args) {
		// Se definiran las transiciones
		List<Transicion> transitions = new ArrayList<>();
		transitions.add(new Transicion("q0", '0', 'X', 1, "q1"));
		transitions.add(new Transicion("q1", '0', '0', 1, "q1"));
		transitions.add(new Transicion("q1", '1', 'Y', 1, "q2"));
		transitions.add(new Transicion("q2", '0', '0', -1, "q2"));
		transitions.add(new Transicion("q2", 'X', 'X', 1, "q0"));
		transitions.add(new Transicion("q0", 'Y', 'Y', 1, "q3"));
		transitions.add(new Transicion("q3", 'Y', 'Y', 1, "q3"));
		transitions.add(new Transicion("q3", ' ', ' ', 0, "accept"));
		transitions.add(new Transicion("q0", ' ', ' ', 0, "accept"));

		// Creamos instancia de la clase MaquinaTuring y ejecutar la Máquina de Turing.
		MaquinaTuring tm = new MaquinaTuring("0010", ' ', transitions);
		tm.ejecutar();
	}
}

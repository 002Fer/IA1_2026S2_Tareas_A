
% ==============================================================================
% MOTOR DE INFERENCIA EN PROLOG (inventario.pl)
% Tarea 2 - Inteligencia Artificial 1
% ==============================================================================

% ------------------------------------------------------------------------------
% 1. DEFINICIÓN DE HECHOS
% ------------------------------------------------------------------------------

% items_principales/1: Hecho que contiene la lista de ítems principales del aventurero.
% Aridad: 1 (acepta un argumento que es una lista con al menos 4 elementos y al menos 1 duplicado).
items_principales([
    espada,
    pocion,
    escudo,
    pocion
]).

% items_secundarios/1: Hecho que contiene la lista de ítems secundarios del aventurero.
% Aridad: 1 (acepta un argumento que es una lista con al menos 3 elementos distintos).
items_secundarios([
    arco,
    mapa,
    llave
]).


% ------------------------------------------------------------------------------
% 2. REGLA DE RECORRIDO RECURSIVO
% ------------------------------------------------------------------------------

% mostrar_inventario/1: Predicado recursivo para imprimir cada elemento de una lista en consola.
% Aridad: 1 (recibe como argumento la lista de ítems a recorrer).

% Caso Base: Maneja la lista vacía [].
% Lógica: Cuando la lista se vacía, la recursión se detiene con éxito sin realizar ninguna acción extra.
mostrar_inventario([]).

% Caso Recursivo: Desestructura la lista en [Cabeza | Cola].
% Lógica: 
% 1. Desestructura la lista extrayendo el primer elemento (Cabeza) y el resto (Cola).
% 2. Imprime el ítem actual en la consola del servidor usando writeln/1.
% 3. Realiza la llamada recursiva pasándole la Cola restante de la lista.
mostrar_inventario([Cabeza | Cola]) :-
    writeln(Cabeza),               % Imprime el ítem actual de la Cabeza en la consola
    mostrar_inventario(Cola).      % Llamada recursiva con la Cola de la lista


% ------------------------------------------------------------------------------
% 3. REGLA PRINCIPAL DE PROCESAMIENTO
% ------------------------------------------------------------------------------

% procesar_inventario/5: Regla principal que procesa el inventario general del aventurero.
% Aridad: 5 
%   - Argumento 1 (Entrada): ItemBuscado (Átomo a verificar en el inventario).
%   - Argumento 2 (Salida): TotalItems (Cantidad total de elementos).
%   - Argumento 3 (Salida): InventarioInvertido (Lista invertida).
%   - Argumento 4 (Salida): InventarioUnico (Lista ordenada sin duplicados).
%   - Argumento 5 (Salida): InventarioOrdenado (Lista ordenada conservando duplicados).

procesar_inventario(ItemBuscado, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado) :-
    items_principales(Principales),                             % Obtiene la lista de ítems principales ([espada, pocion, escudo, pocion])
    items_secundarios(Secundarios),                             % Obtiene la lista de ítems secundarios ([arco, mapa, llave])
    append(Principales, Secundarios, InventarioGeneral),        % append/3: Concatena Principales y Secundarios en InventarioGeneral
    length(InventarioGeneral, TotalItems),                      % length/2: Calcula la cantidad total de elementos en InventarioGeneral
    member(ItemBuscado, InventarioGeneral),                     % member/2: Verifica por unificación que ItemBuscado exista en el inventario
    reverse(InventarioGeneral, InventarioInvertido),            % reverse/2: Invierte el orden de los elementos de InventarioGeneral
    sort(InventarioGeneral, InventarioUnico),                   % sort/2: Ordena alfabéticamente y elimina elementos duplicados
    msort(InventarioGeneral, InventarioOrdenado),               % msort/2: Ordena alfabéticamente conservando elementos duplicados
    mostrar_inventario(InventarioGeneral).                      % Llamada al predicado recursivo mostrar_inventario/1 como última instrucción
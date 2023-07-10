

TIPO_DOCUMENTO = [
    {
        'descricao': 'Atestado',
        'id': 16,
        'metadata': {},
        'sigla': 'ATS'},
    {
        'descricao': 'Comunicação Interna',
        'id': 7,
        'metadata': {},
        'sigla': 'CI'},
    {
        'descricao': 'Comunicado',
        'id': 9,
        'metadata': {},
        'sigla': 'CO'},
    {
        'descricao': 'Convite',
        'id': 1,
        'metadata': {},
        'sigla': 'CNV'},
    {
        'descricao': 'Declaração',
        'id': 13,
        'metadata': {},
        'sigla': 'DCL'},
    {
        'descricao': 'Documento',
        'id': 17,
        'metadata': {},
        'sigla': 'DOC'},
    {
        'descricao': 'E-mail',
        'id': 18,
        'metadata': {},
        'sigla': 'EM'},
    {
        'descricao': 'Informe',
        'id': 10,
        'metadata': {},
        'sigla': 'INF'},
    {
        'descricao': 'Oficio',
        'id': 2,
        'metadata': {},
        'sigla': 'OFC'},
    {
        'descricao': 'Ofício Circular',
        'id': 8,
        'metadata': {},
        'sigla': 'OC'},
    {
        'descricao': 'Ofício Expedido',
        'id': 15,
        'metadata': {},
        'sigla': 'OE'},
    {
        'descricao': 'Parecer',
        'id': 5,
        'metadata': {},
        'sigla': 'PAR'},
    {
        'descricao': 'Projeto de Lei',
        'id': 4,
        'metadata': {},
        'sigla': 'PL'},
    {
        'descricao': 'Requerimento',
        'id': 3,
        'metadata': {},
        'sigla': 'REQ'},
    {
        'descricao': 'Resposta de Ofício',
        'id': 12,
        'metadata': {},
        'sigla': 'RO'},
    {
        'descricao': 'Resposta de Requerimento',
        'id': 6,
        'metadata': {},
        'sigla': 'RR'},
    {
        'descricao': 'Solicitação',
        'id': 11,
        'metadata': {},
        'sigla': 'SOL'}
]

TIPO_MATERIA = [
    {
        'descricao': 'Indicação',
        'id': 8,
        'metadata': {},
        'sigla': 'IND'},
    {
        'descricao': 'Parecer de Comissão',
        'id': 4,
        'metadata': {},
        'sigla': 'PAR'},
    {
        'descricao': 'Projeto de Decreto Legislativo',
        'id': 6,
        'metadata': {},
        'sigla': 'PDL'},
    {
        'descricao': 'Projeto de Lei Complementar do Executivo',
        'id': 5,
        'metadata': {},
        'sigla': 'PLCE'},
    {
        'descricao': 'Projeto de Lei Complementar do Legislativo',
        'id': 11,
        'metadata': {},
        'sigla': 'PLCL'},
    {
        'descricao': 'Projeto de Lei do Executivo',
        'id': 1,
        'metadata': {},
        'sigla': 'PLE'},
    {
        'descricao': 'Projeto de Lei do Legislativo',
        'id': 9,
        'metadata': {},
        'sigla': 'PLL'},
    {
        'descricao': 'Projeto de Resolução',
        'id': 2,
        'metadata': {},
        'sigla': 'PRE'},
    {
        'descricao': 'Requerimento',
        'id': 3,
        'metadata': {},
        'sigla': 'REQ'},
    {
        'descricao': 'Veto',
        'id': 10,
        'metadata': {},
        'sigla': 'VT'},
    {
        'descricao': 'Requerimento de Vereador(a)',
        'id': 13,
        'metadata': {},
        'sigla': 'RV'},
    {
        'descricao': 'Emenda',
        'id': 15,
        'metadata': {},
        'sigla': 'EM'},
    {
        'descricao': 'Projeto de Emenda à Lei Orgânica Muncipal',
        'id': 16,
        'metadata': {},
        'sigla': 'PELOM'}
]

DOCUMENTO = {t['id']: {'descricao' : t['descricao'], 'sigla' : t['sigla']} for t in TIPO_DOCUMENTO}
MATERIA = {t['id']: {'descricao' : t['descricao'], 'sigla' : t['sigla']} for t in TIPO_MATERIA}
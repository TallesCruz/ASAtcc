$(document).ready(function() {
    $.fn.dataTable.luxon('dd/MM/yyyy');
    
    $('#tabela').dataTable({
         language: {
            url: '//cdn.datatables.net/plug-ins/1.10.22/i18n/Portuguese-Brasil.json', 
            searchBuilder: {
                title: {
                    0: 'Filtro customizado',
                    _: 'Filtros (%d)'
                },
                logicAnd: 'Se',
                logicOr: 'Ou',
                clearAll: 'Limpar tudo',
                add: '+',
                data: 'Coluna',
                value: 'Valor',
                condition: 'Condiçâo',
                conditions :{
                        number:{
                    equals: 'Igual',
                    not: 'Diferente',
                    lt: 'Menor que',
                    lte: 'Menor que, igual',
                    gte: 'Maior que, igual',
                    gt: 'Maior que',
                            between: 'Entre',
                    notBetween: 'Diferente entre',
                    empty: 'Vazio',
                    notEmpty: 'Não vazio',
                         }, 
                        string: {
                            contains: 'Contém',
                            empty: 'Vazio',
                            endsWith: 'Termina com',
                            equals: 'Igual',
                            not: 'Diferente',
                            notContains: 'Não contém',
                            notEmpty: 'Não vazio',
                            notEndsWith: 'Não termina com',
                            notStartsWith: 'Não começa com',
                            startsWith: 'Começa com',
                          },
                        date: {
                            after: 'Depois',
                            before: 'Antes',
                            between: 'Entre',
                    empty: 'Vazio',
                    equals: 'Igual',
                            not: 'Não',
                    notBetween: 'Não entre',
                    notEmpty: 'Não vazio',
                        },
                    
                    }
                }
            },
            dom: 'Qlfrtip',
            columnDefs: [ {
                    "targets": 2,
                    type : 'date'
                    } ]
    });
    });
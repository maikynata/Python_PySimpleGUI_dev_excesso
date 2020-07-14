select prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, prun_estmin  from produtos, produn
where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' and prod_codigo in (101567,649848,590045)

select prod_descricao, prod_complemento, prod_marca, prun_prvenda, prun_estoque1, prun_estmin  from produtos, produn
where prod_codigo=prun_prod_codigo and prun_unid_codigo='001' and prod_codigo in (select cbal_prod_codigo from cbalt where cbal_prod_codbarras='7891182029827')


update produn
set prun_estmin=2
where prun_unid_codigo='001' and prun_prod_codigo=101567

-- Transacao nextVal
SELECT NextVal(CONCAT('transacao','002')) As Proximo

select unid_codigo from unidades
where unid_codigo='002'

-- Insert PENDEST
select * from pendest limit 10

select * from pendest 
where Pest_DataMvto = '2020-07-13'

INSERT INTO PendEst (pest_operacao, pest_transacao, pest_status, pest_datamvto, pest_unid_origem, pest_unid_destino, pest_prod_codigo, pest_cpes_codigo, pest_cpes_tipo, pest_catentidade, pest_codEntidade, pest_sequencial, pest_valor, pest_qemb, pest_qtde, pest_qtdebx, pest_transacaobx, pest_bxcompleta, Pest_DataBaixa, Pest_CtCompra, Pest_CtFiscal, Pest_CtEmpresa, Pest_CtTransf, Pest_Espe_Codigo, Pest_DataValidade, Pest_DataEntrega) VALUES('001177212711', '00117721271', 'P', CAST('2020-07-04' AS DATE), '002', '001', 100005, '001', 'PI', 'N', 0, 1, 10.27, 0, 1, 0, '', '', CAST(null AS DATE), 11.50228, 11.50228, 11.50228, 12.52944, '', CAST(null AS DATE), CAST(null AS DATE))

--INSERT INTO PendEst (Pest_Operacao, Pest_Transacao, Pest_Status, Pest_DataMvto, Pest_Unid_Destino, Pest_Unid_Origem, Pest_Prod_Codigo, Pest_Cpes_Codigo, Pest_Cpes_Tipo, Pest_CatEntidade, Pest_CodEntidade, Pest_Espe_Codigo, Pest_Sequencial, Pest_Valor, Pest_Qtde, Pest_QEmb, Pest_QtdeBx, Pest_TransacaoBx, Pest_DataBaixa, Pest_ICMS, Pest_PercRedBC, Pest_SimbICMS, Pest_CtCompra, Pest_CtFiscal, Pest_CtEmpresa, Pest_CtTransf, Pest_CtMedio) VALUES('001177213443', '00117721344', 'P', CAST('2020-07-04' AS DATE), '001', '001', 169935, '005', 'TC', 'F', 100021, '', 1, 25.56, 1, 0, 0, '', CAST(null AS DATE), 0, 0, 'OT', 25.5601, 25.5601, 25.5601, 28.4, 25.1598)
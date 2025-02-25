SQL_APAGAR_TABELA_USUARIO = """
    DROP TABLE IF EXISTS usuario
"""

SQL_CRIAR_TABELA_USUARIO = """
    CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    data_nascimento DATE, 
    data_criacao TEXT NOT NULL,
    nome_perfil TEXT NOT NULL,
    foto_perfil BOOL,
    bio_perfil TEXT,
    genero TEXT,
    status TEXT NOT NULL )   
"""

SQL_INSERIR_USUARIO = """
    INSERT INTO usuario 
    (nome, email, senha, data_criacao, nome_perfil, status)
    VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_ATUALIZAR_DATA = """
    UPDATE usuario
    SET data_nascimento = ?,
    WHERE EMAIL = ?
"""

SQL_OBTER_DADOS_PERFIL = """
    SELECT bio_perfil, genero
    FROM usuario
    WHERE id = ?
"""

SQL_OBTER_DADOS_PERFIL_VISITADO = """
    SELECT id, nome, nome_perfil, bio_perfil, categoria_perfil, foto_perfil
    FROM usuario
    WHERE id = ?
"""

SQL_OBTER_DADOS_PERFIL_SEGUIDO = """
    SELECT id, nome_perfil, foto_perfil
    FROM usuario
    WHERE id = ?
"""

SQL_ATUALIZAR_CATEGORIA_PERFIL = """
    UPDATE usuario
    SET categoria_perfil = ?
    WHERE email = ?
"""

SQL_ATUALIZAR_DADOS = """
    UPDATE usuario
    SET foto_perfil = ?, nome = ?, nome_perfil = ?, bio_perfil = ?, genero = ?
    WHERE id = ?
"""

SQL_CHECAR_CREDENCIAIS = """
    SELECT id, nome, senha, nome_perfil, foto_perfil
    FROM usuario
    WHERE email = ?
"""

SQL_CHECAR_ID = """
    SELECT id FROM usuario WHERE email = ?
"""

SQL_CHECAR_FOTO_PERFIL = """
    SELECT foto_perfil FROM usuario WHERE id = ?
"""
SQL_CHECAR_EMAIL_UNICO = """SELECT 1 FROM usuario WHERE email = ?"""

SQL_CHECAR_CPF_UNICO = """SELECT 1 FROM usuario WHERE cpf = ?"""

SQL_CHECAR_TELEFONE_UNICO = """SELECT 1 FROM usuario WHERE telefone = ?"""

SQL_CHECAR_NOME_PERFIL_UNICO = """SELECT 1 FROM usuario WHERE nome_perfil = ?"""

SQL_ATUALIZAR_SENHA = """
    UPDATE usuario
    SET senha = ?
    WHERE email = ?
"""

SQL_FAZER_UPGRADE_PLANO = """
    UPDATE usuario
    SET tipo_paciente = ?
    WHERE email = ?
"""

SQL_EXCLUIR_USUARIO = """
    DELETE FROM usuario
    WHERE email = ?
"""

SQL_PESQUISAR_USUARIOS = """
    SELECT id, nome, nome_perfil, foto_perfil 
    FROM usuario 
    WHERE nome_perfil LIKE ?
"""
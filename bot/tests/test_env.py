def test_env():
    from rift import env

    assert env.ENVIRONMENT == "dev"
    assert env.PROD_APPLICATION_ID == 1
    assert env.PROD_TOKEN == "abc123"
    assert env.BETA_APPLICATION_ID == 2
    assert env.BETA_TOKEN == "def456"
    assert env.DEV_APPLICATION_ID == 3
    assert env.DEV_TOKEN == "ghi789"
    assert env.DEV_GUILD_IDS == [1, 2, 3]
    assert env.DB_HOST == "localhost"
    assert env.DB_PORT == 5432
    assert env.DB_USER == "postgres"
    assert env.DB_PASSWORD == "postgres"
    assert env.DB_NAME == "postgres"

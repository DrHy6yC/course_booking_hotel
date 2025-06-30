def create_trigger_function(table_name, column):
    return f"""
CREATE OR REPLACE FUNCTION set_{table_name}_{column}()
RETURNS TRIGGER AS $$
BEGIN
    NEW.{column} = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""


def create_update_trigger(table_name, column, type_before):
    return f"""
    CREATE TRIGGER {table_name}_{type_before}_timestamp
    BEFORE {type_before} ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION set_{table_name}_{column}();
    """

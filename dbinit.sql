CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance INT8
);

--or just in container terminal:
--cockroach sql --insecure -e "CREATE TABLE accounts (id UUID PRIMARY KEY, balance INT8);"

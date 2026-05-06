-- =========================
-- Таблица пользователей
-- =========================
CREATE TABLE users (
    id          SERIAL PRIMARY KEY,
    vk_id       BIGINT UNIQUE NOT NULL,
    name        VARCHAR(100) NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_vk_id ON users (vk_id);

-- =========================
-- Таблица семей
-- =========================
CREATE TABLE families (
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    invite_code  VARCHAR(32) UNIQUE NOT NULL,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_families_invite_code ON families (invite_code);

-- =========================
-- Таблица участников семьи
-- =========================
CREATE TABLE family_members (
    id         SERIAL PRIMARY KEY,
    user_id    INT NOT NULL,
    family_id  INT NOT NULL,
    role       VARCHAR(20) NOT NULL CHECK (role IN ('owner', 'parent', 'child')),
    joined_at  TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_family_members_user
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_family_members_family
        FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT uq_family_members UNIQUE (user_id, family_id)
);

CREATE INDEX idx_family_members_user ON family_members (user_id);
CREATE INDEX idx_family_members_family ON family_members (family_id);

-- =========================
-- Таблица задач
-- =========================
CREATE TABLE tasks (
    id           SERIAL PRIMARY KEY,
    family_id    INT NOT NULL,
    creator_id   INT, 
    assigned_to  INT,
    title        VARCHAR(255) NOT NULL,
    description  TEXT,
    status       VARCHAR(20) NOT NULL
                 CHECK (status IN ('new', 'in_progress', 'done')),
    deadline     TIMESTAMP,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_tasks_family
        FOREIGN KEY (family_id) REFERENCES families (id) ON DELETE CASCADE,
    CONSTRAINT fk_tasks_creator
        FOREIGN KEY (creator_id) REFERENCES users (id) ON DELETE SET NULL,
    CONSTRAINT fk_tasks_assigned
        FOREIGN KEY (assigned_to) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX idx_tasks_family ON tasks (family_id);
CREATE INDEX idx_tasks_assigned ON tasks (assigned_to);
CREATE INDEX idx_tasks_status ON tasks (status);

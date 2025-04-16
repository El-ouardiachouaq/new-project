from app import db
from app import User

def upgrade():
    # Add reset token fields
    db.session.execute('ALTER TABLE user ADD COLUMN reset_token VARCHAR(100) UNIQUE')
    db.session.execute('ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME')
    db.session.commit()

def downgrade():
    # Remove reset token fields
    db.session.execute('ALTER TABLE user DROP COLUMN reset_token')
    db.session.execute('ALTER TABLE user DROP COLUMN reset_token_expiry')
    db.session.commit()

if __name__ == '__main__':
    upgrade() 
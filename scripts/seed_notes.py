from crunevo import create_app, db, User, Note

app = create_app()

with app.app_context():
    # Create sample user if not exists
    user = User.query.filter_by(username="demo").first()
    if not user:
        user = User(username="demo", email="demo@example.com", name="Demo User")
        user.set_password("demo")
        db.session.add(user)
        db.session.commit()
        print("Created demo user")

    # Create sample notes if none exist
    if Note.query.count() == 0:
        sample_note = Note(
            title="Ejemplo de Apunte",
            description="Apunte de prueba para el feed",
            file_url="https://example.com/sample.pdf",
            file_type="pdf",
            user_id=user.id,
            course="Curso 101",
            faculty="Facultad de Ejemplo",
        )
        db.session.add(sample_note)
        db.session.commit()
        print("Inserted sample note")
    else:
        print("Notes already exist, skipping.")

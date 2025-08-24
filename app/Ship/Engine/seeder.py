from app.Containers.User.Data.Seeders.SuperAdminSeeder import SuperAdminSeeder

def run_seeders():
    """Run all database seeders"""
    print("Running database seeders...")
    
    # Run super admin seeder
    super_admin_seeder = SuperAdminSeeder()
    super_admin_seeder.run()
    
    print("Seeders completed successfully!")

if __name__ == "__main__":
    run_seeders()
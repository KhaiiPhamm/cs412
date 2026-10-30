"""
    File: models.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 10/30/2026
    Description: Stores each voter's profile information and 
    maps those fields to database columns
"""

from django.db import models
from datetime import date
# Create your models here.

class Voter(models.Model):
    """Voter class"""
    
    first_name = models.TextField()
    last_name = models.TextField()

    street_number = models.CharField(max_length=20)
    street_name = models.TextField()
    zip_code = models.CharField(max_length=10)

    dob = models.DateField()
    
    party_affiliation = models.CharField(max_length=2)
    registration_date = models.DateField()
    
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"
    
def load_data():
    """Function to load data records from CSV file into Django model instances. """
    
    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = '/Users/pdkha/Documents/Classes/Fall 2026/CS412/django/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
    
    voters = []
    
    for line in f:
        fields = line.strip().split(',')
        # show which value in each field
        
        try:
            dob = date.fromisoformat(fields[7])
            registration = date.fromisoformat(fields[8])
            # create a new instance of Result object with this record from CSV
            voter = Voter(first_name = fields[2],
                            last_name = fields[1],
                            street_number = fields[3],
                            street_name = fields[4],
                            zip_code = fields[6],
                            dob = dob,
                            registration_date= registration,
                            party_affiliation = fields[9].strip(),
                            v20state = (fields[11] == 'TRUE'),
                            v21town = (fields[12] == 'TRUE'),
                            v21primary = (fields[13] == 'TRUE'),
                            v22general = (fields[14] == 'TRUE'),
                            v23town = (fields[15] == 'TRUE'),
                            voter_score = int(fields[16]),
                            )
            voters.append(voter)
        except Exception as e:
            print(f"Skipped: {fields} ({e})")
    f.close()
    Voter.objects.bulk_create(voters, batch_size=1000)
    print(f'Done. Created {len(Voter.objects.all())} Voters.')
            
        
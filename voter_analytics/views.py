"""
    File: views.py
    Author: Khai Duc Pham (khaipduc@bu.edu), 10/30/2026
    Description: View functions for the voter_analytic app. 
"""
from django.views.generic import ListView, DetailView
from datetime import date
from collections import Counter
import plotly
import plotly.graph_objects as go
from . models import Voter

class VotersListView(ListView):
    """View to display voter records"""
    
    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100 
    
    def get_queryset(self):
        
        # start with entire queryset
        voters = super().get_queryset().order_by('last_name', 'first_name')
        
        # filter results by these field(s):
        if 'party_aff' in self.request.GET:
            party_aff = self.request.GET['party_aff']
            if party_aff:
                voters = voters.filter(party_affiliation=party_aff)

        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                voters = voters.filter(dob__gte=date(int(min_dob), 1, 1))

        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(dob__lte=date(int(max_dob), 12, 31))

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(voter_score=voter_score)

        if self.request.GET.get('v20state'):
            voters = voters.filter(v20state=True)

        if self.request.GET.get('v21town'):
            voters = voters.filter(v21town=True)

        if self.request.GET.get('v21primary'):
            voters = voters.filter(v21primary=True)

        if self.request.GET.get('v22general'):
            voters = voters.filter(v22general=True)

        if self.request.GET.get('v23town'):
            voters = voters.filter(v23town=True)              
        
        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # every party code that exists in the data, sorted
        context['parties'] = ['A', 'AA', 'CC', 'D', 'E', 'EE', 'FF', 'G', 'GG', 'H', 'HH',
                      'J', 'K', 'L', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                      'X', 'Y', 'Z']
        context['years'] = range(1913, 2006)
        context['scores'] = range(0, 6)
        params = self.request.GET.copy()
        params.pop('page', None)
        context['query_string'] = params.urlencode()
        return context  


class VoterDetailView(DetailView):
    '''View to show detail page for one voter.'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'v'

class GraphsListView(VotersListView):
    '''View to display graphs of the (filtered) voter records'''

    template_name = 'voter_analytics/graphs.html'
    paginate_by = None
    
    def get_context_data(self, **kwargs):
        '''
        Provide context variables for use in template
        '''

        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()
        n = voters.count()

        # graph 1: bar chart of voters by year of birth
        birth_years = Counter()
        for dob in voters.values_list('dob', flat=True):
            birth_years[dob.year] += 1
        years = sorted(birth_years)
        counts = [birth_years[y] for y in years]

        fig = go.Bar(x=years, y=counts)
        title_text = f"Voter distribution by Year of Birth (n={n})"
        graph_div_birth = plotly.offline.plot({"data": [fig],
                                               "layout_title_text": title_text,
                                               },
                                              auto_open=False,
                                              output_type="div")
        context['graph_div_birth'] = graph_div_birth

        # graph 2: pie chart of voters by party affiliation
        parties = Counter(voters.values_list('party_affiliation', flat=True))

        fig = go.Pie(labels=list(parties.keys()), values=list(parties.values()))
        title_text = f"Voter distribution by Party Affiliation (n={n})"
        graph_div_party = plotly.offline.plot({"data": [fig],
                                               "layout_title_text": title_text,
                                               },
                                              auto_open=False,
                                              output_type="div")
        context['graph_div_party'] = graph_div_party

        # graph 3: bar chart of how many voted in each election
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [
            voters.filter(v20state=True).count(),
            voters.filter(v21town=True).count(),
            voters.filter(v21primary=True).count(),
            voters.filter(v22general=True).count(),
            voters.filter(v23town=True).count(),
        ]

        fig = go.Bar(x=elections, y=election_counts)
        title_text = f"Vote Count by Election (n={n})"
        graph_div_elections = plotly.offline.plot({"data": [fig],
                                                   "layout_title_text": title_text,
                                                   },
                                                  auto_open=False,
                                                  output_type="div")
        context['graph_div_elections'] = graph_div_elections

        return context
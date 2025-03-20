from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from videos.models import Video, User, UserVideoHistory
########################################################
###Unit test videos Popular
########################################################
class PopularVideosTestsUnit(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='pabloraul@', password='Jpcasa@@72')
        cls.client = Client()
        
        # Crear videos con diferentes características
        cls.videos = [
            #0
            Video.objects.create(
                title='Regueton bad bunny',
                embed_link='https://www.youtube.com/embed/NKVI1zbtLHY',
                created_at=timezone.now(),
                user=cls.user
            ),
            #1
            Video.objects.create(
                title='salsa marc anthony',
                embed_link='https://www.youtube.com/embed/xHC5y35GtqU',
                created_at=timezone.now() - timedelta(days=1),
                user=cls.user
            ),
            #2
            Video.objects.create(
                title='Sandy papo MERENGUE',
                embed_link='https://www.youtube.com/embed/iEn6jXJuWIw',
                created_at=timezone.now() - timedelta(days=35),
                user=cls.user
            ),
            #3
            Video.objects.create(
                title='LINKIN PARK',
                embed_link='https://www.youtube.com/embed/dxytyRy-O1k',
                created_at=timezone.now() - timedelta(days=35),
                user=cls.user
            )
        ]

    def test_popularity_calculation(self):
        # Simular interacciones y agregar puntos 
        #video1
        self.videos[0].likes.add(self.user)  # +10
        self.videos[0].dislikes.add(self.user)  # -5 (net +5)
        self.videos[0].comments.create(user=self.user, content="Test")  # +1
        #video2
        self.videos[1].likes.add(self.user)  # +10
        self.videos[1].likes.add(self.user)  # Duplicado no cuenta
        self.videos[1].comments.create(user=self.user, content="Test")  # +1
        #video 3 no tuvo punto
        #video 4        
        self.videos[3].comments.create(user=self.user, content="Test")  # +1
        
        response = self.client.get(reverse('popular_videos')) 
        
        
########################################################
###Unit test videos history
######################################################## 
class VideoHistoryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='pabloraul1@', email='testuser@example.com', password='Jpcasa@@72')
        cls.other_user = User.objects.create_user(username='Jpablo@', email='2testuser@example.com', password='Jpcasa@@72')
        cls.client = Client()   
        # Crear videos y historial
        cls.video = Video.objects.create(
            title='video bad bunny',
            embed_link='https://www.youtube.com/embed/NKVI1zbtLHY',
            user=cls.user
        )
        # Crear 15 entradas de historial
        for i in range(15):
            UserVideoHistory.objects.create(
                user=cls.user,
                video=cls.video,
                viewed_at=timezone.now() - timedelta(minutes=i),      
            )  
    def test_authentication_required(self):
        response = self.client.get(reverse('view_history'))
        self.assertEqual(response.status_code, 302)  # Redirección a login

    def test_pagination(self):
        self.client.login(username='pabloraul1@', password='Jpcasa@@72')
        response = self.client.get(reverse('view_history'))
        if response.context['history'] is not None:
            self.assertTrue(response.context['history'].has_other_pages())
            self.assertEqual(len(response.context['history']), 10)

    def test_ordering(self):
        self.client.login(username='pabloraul1@', password='Jpcasa@@72')
        response = self.client.get(reverse('view_history'))
        
        history = response.context['history']
        self.assertTrue(
            history[0].viewed_at > history[1].viewed_at,
            msg="El historial debe estar ordenado de más reciente a más antiguo"
        )

    def test_user_specific_history(self):
    # Crear entrada para otro usuario
        UserVideoHistory.objects.create(
            user=self.other_user,
            video=self.video,
            viewed_at=timezone.now()
        )
        self.client.login(username='pabloraul1@', password='Jpcasa@@72')
        response = self.client.get(reverse('view_history'))      
        user_history = response.context['history'].object_list
        self.assertTrue(all(entry.user == self.user for entry in user_history))

    def test_view_tracking(self):
        self.client.login(username='Jpablo@', password='Jpcasa@@72')    
        # Ver video por primera vez
        self.client.get(reverse('video_detail', args=[self.video.id]))
        initial_count = UserVideoHistory.objects.filter(user=self.user).count()  
        # Ver video nuevamente
        self.client.get(reverse('video_detail', args=[self.video.id]))
        
        
    
   
   
             
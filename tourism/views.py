# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

# Sample data (images are public Wikimedia URLs)
CAROUSEL = [
    {"url": "https://imgs.search.brave.com/wTuFQ08iHd60fn6o039gZReymeT0SnTgp_sIy4QswoI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9leHRl/cm5hbC1wcmV2aWV3/LnJlZGQuaXQvaHVu/ZHJ1LWZhbGwtcmFu/Y2hpLXYwLWFXSTJj/bkZzZERoemJXRm1N/WUhuUjRSc0VwRHNt/RGhpVUM5dFpYR2sy/ZUVBN2QyZS04UUhh/NG9Mb2tIdi5wbmc_/d2lkdGg9NjQwJmNy/b3A9c21hcnQmZm9y/bWF0PXBqcGcmYXV0/bz13ZWJwJnM9ZmJm/ODc1N2I2YmM3Zjc2/YzA1YzNhZTVkYTAz/NDQwYjhlMGM1ZjU2/Mg", "title": "Hundru Falls", "caption": "A spectacular waterfall in Ranchi"},
    {"url": "https://imgs.search.brave.com/ncSjoJ4bdvl0TD5G_uXmO_KCEbIckhrGdXsL9WrFpco/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zN2Fw/MS5zY2VuZTcuY29t/L2lzL2ltYWdlL2lu/Y3JlZGlibGVpbmRp/YS9iYWJhLWJhaWR5/YW5hdGgtZGhhbS1k/ZW9naGFyLW9kaXNo/YS10cmktaGVyby0x/P3FsdD04MiZ0cz0x/NzI3MTYzODU1Mzg3", "title": "Baidyanath Temple", "caption": "Pilgrimage center in Deoghar"},
    {"url": "https://imgs.search.brave.com/Q6_yBQ6dZmrI3FerzVVYdTySM9Y7fCuouHK8-cKIHfg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zN2Fw/MS5zY2VuZTcuY29t/L2lzL2ltYWdlL2lu/Y3JlZGlibGVpbmRp/YS9qdWJpbGVlLXBh/cmstamFtc2hlZHB1/ci1qaGFya2hhbmQt/MS1jaXR5LWhvbWVw/YWdlP3FsdD04MiZ0/cz0xNzQyMTU1NTI2/MTc4", "title": "Jubilee Park", "caption": "Green oasis in Jamshedpur"},
    {"url": "https://imgs.search.brave.com/6r3O3tocbs5Q2hid5sx10JyKaJcw4ynTqsYzt5Vy8lI/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vd3d3Lm9w/aW5kaWEuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDI1LzA3/L1BhbGFtdS10d2lu/LWZvcnRzLXRvLWJl/LXJlc3RvcmVkXy1K/aGFya2hhbmQucG5n/P3Jlc2l6ZT02OTYs/Mzk4JnNzbD0x", "title": "Palamu Fort", "caption": "Historic Palamu Fort"},
    {"url": "https://imgs.search.brave.com/FWH_glN6aQr89NbkEGbe4ih1lCJWauxp6IRgTa0_eyA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cmFuY2hpbXVuaWNp/cGFsLmNvbS9pbWFn/ZXMvcm9ja2dhcmRl/bi5qcGc","title":"Rock Garden","caption":"Scenic viewpoint"}
]

# Data for "Experiences" section, inspired by the reference site
EXPERIENCES = [
    {"name": "Waterfalls", "image": "https://imgs.search.brave.com/wTuFQ08iHd60fn6o039gZReymeT0SnTgp_sIy4QswoI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9leHRl/cm5hbC1wcmV2aWV3/LnJlZGQuaXQvaHVu/ZHJ1LWZhbGwtcmFu/Y2hpLXYwLWFXSTJj/bkZzZERoemJXRm1N/WUhuUjRSc0VwRHNt/RGhpVUM5dFpYR2sy/ZUVBN2QyZS04UUhh/NG9Mb2tIdi5wbmc_/d2lkdGg9NjQwJmNy/b3A9c21hcnQmZm9y/bWF0PXBqcGcmYXV0/bz13ZWJwJnM9ZmJm/ODc1N2I2YmM3Zjc2/YzA1YzNhZTVkYTAz/NDQwYjhlMGM1ZjU2/Mg"},
    {"name": "Temples", "image": "https://imgs.search.brave.com/ncSjoJ4bdvl0TD5G_uXmO_KCEbIckhrGdXsL9WrFpco/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zN2Fw/MS5zY2VuZTcuY29t/L2lzL2ltYWdlL2lu/Y3JlZGlibGVpbmRp/YS9iYWJhLWJhaWR5/YW5hdGgtZGhhbS1k/ZW9naGFyLW9kaXNo/YS10cmktaGVyby0x/P3FsdD04MiZ0cz0x/NzI3MTYzODU1Mzg3"},
    {"name": "Wildlife", "image": "https://imgs.search.brave.com/l7Z6O3JehCLRjFLTy6nu7F7rwe--pdOdFyZunvZZ42A/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbS5o/dW50LmluL2NnL2po/YXIvQWJvdXQvVG91/cmlzbS93aWxnLmpw/Zw"},
    {"name": "Hills", "image": "https://imgs.search.brave.com/8b_zKXaNLataHfK_IkVbeOOTgi4QJVYkfVRj3tq_lGY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzA2LzQ0LzkwLzQy/LzM2MF9GXzY0NDkw/NDI4OV9OYlhLVEtJ/U05sY3BuNnR0QjJQ/M3VwbzFJSVBxcGVL/RS5qcGc"},
    {"name": "Dams", "image": "https://imgs.search.brave.com/gFO0KSMQsF1EaHwnF0DYEiGH2l6A4dQAxJBHzAy4lOQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9jZG4u/czN3YWFzLmdvdi5p/bi9zM2UxNjU0MjEx/MTBiYTAzMDk5YTFj/MDM5MzM3M2M1YjQz/L3VwbG9hZHMvYmZp/X3RodW1iLzIwMTgw/NDIzNjUtb2x3ZDZu/NW5wcWQ1aHg1YTVs/MmExNG41d2t6bGJo/Z3BpMXd4djVpYWg2/LmpwZw"},
    {"name": "Culture", "image": "https://imgs.search.brave.com/IPIiQjAgE8hY8DVjGnSzxN82rURE3NQXc6O0NiFEeHM/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbS5o/dW50LmluL2NnL2po/YXIvQWJvdXQvUHJv/ZmlsZS9LYXJhbUZl/c3RpdmFsSmhhcmto/YW5kLmpwZw"},
    {"name": "Adventure", "image": "https://imgs.search.brave.com/e94_IrsFlS9uQQmSCoQwX6j3sAwUKa0OW31EdO7yVmo/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pbS5o/dW50LmluL2NnL3Jh/bmNoaS9DaXR5LUd1/aWRlL3JvY2tpZXMu/anBn"},
    {"name": "Heritage", "image": "https://imgs.search.brave.com/AhX_j3euFWbv3Ld3_mdj8xeSfB9HMgdS50_3Ms3n3bY/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9zdGF0/aWMyLnRyaXBvdG8u/Y29tL21lZGlhL2Zp/bHRlci9ubC9pbWcv/MTY5MTU1Ni9Ucmlw/RG9jdW1lbnQvMTU5/MjQ3OTQ5MV8yMDE4/MDUwMjk3X29sd2Iz/Y2I0N2phN2VpaXh2/MWE4YTRwc3BjNTBv/ZWl0dGNnbHQ1NW95/Mi5qcGc"},
    {"name": "Handicrafts", "image": "https://imgs.search.brave.com/feln8ChDyupRT4jEGhTLmdDduHCrt6CS_8_vL1uuaIg/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/aW5kaWFuaGFuZGlj/cmFmdHN0b3JlLmNv/bS93cC1jb250ZW50/L3VwbG9hZHMvMjAy/My8wNC9Ub3AtMTAt/U3VzdGFpbmFibGUt/SGFuZGljcmFmdHMt/b2YtQXNzYW0tMi0x/LTQwMHgyNTAucG5n"},
    {"name": "Cuisine", "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=800&auto=format&fit=crop"}
]

DISTRICTS = [
    {"name":"ranchi", "display":"Ranchi", "slug":"ranchi",
     "image":"https://imgs.search.brave.com/wTuFQ08iHd60fn6o039gZReymeT0SnTgp_sIy4QswoI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9leHRl/cm5hbC1wcmV2aWV3/LnJlZGQuaXQvaHVu/ZHJ1LWZhbGwtcmFu/Y2hpLXYwLWFXSTJj/bkZzZERoemJXRm1N/WUhuUjRSc0VwRHNt/RGhpVUM5dFpYR2sy/ZUVBN2QyZS04UUhh/NG9Mb2tIdi5wbmc_/d2lkdGg9NjQwJmNy/b3A9c21hcnQmZm9y/bWF0PXBqcGcmYXV0/bz13ZWJwJnM9ZmJm/ODc1N2I2YmM3Zjc2/YzA1YzNhZTVkYTAz/NDQwYjhlMGM1ZjU2/Mg",
     "tagline":"Waterfalls & Culture",
     "attractions":[
         {"title":"Hundru Falls","subtitle":"Waterfall near Ranchi","image":"https://imgs.search.brave.com/wTuFQ08iHd60fn6o039gZReymeT0SnTgp_sIy4QswoI/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9leHRl/cm5hbC1wcmV2aWV3/LnJlZGQuaXQvaHVu/ZHJ1LWZhbGwtcmFu/Y2hpLXYwLWFXSTJj/bkZzZERoemJXRm1N/WUhuUjRSc0VwRHNt/RGhpVUM5dFpYR2sy/ZUVBN2QyZS04UUhh/NG9Mb2tIdi5wbmc_/d2lkdGg9NjQwJmNy/b3A9c21hcnQmZm9y/bWF0PXBqcGcmYXV0/bz13ZWJwJnM9ZmJm/ODc1N2I2YmM3Zjc2/YzA1YzNhZTVkYTAz/NDQwYjhlMGM1ZjU2/Mg","desc":"One of the most famous waterfalls in Jharkhand."},
         {"title":"Rock Garden","subtitle":"Scenic viewpoint","image":"https://imgs.search.brave.com/FWH_glN6aQr89NbkEGbe4ih1lCJWauxp6IRgTa0_eyA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly93d3cu/cmFuY2hpbXVuaWNp/cGFsLmNvbS9pbWFn/ZXMvcm9ja2dhcmRl/bi5qcGc","desc":"Park overlooking Kanke Dam."},
         {"title":"Dassam Falls","subtitle":"Waterfall near Ranchi","image":"https://www.holidify.com/images/cmsuploads/compressed/Dassam_Falls_20190211152927.jpg","desc":"A beautiful waterfall with a 44-meter drop."},
         {"title":"Jagannath Temple","subtitle":"Replica of Puri temple","image":"https://www.tourmyindia.com/states/jharkhand/images/jagannath-temple1-1.jpg","desc":"Historic temple built in 1691."}
     ],
     "food":["Handia","Bamboo Shoot Curry","Thekua"],
     "handicrafts":["Dokra","Bamboo crafts"],
     "stays":["Hotels","Homestays","Eco-lodges"]
    },
    {"name":"palamu","display":"Palamu", "slug":"palamu",
    "image": "https://imgs.search.brave.com/6r3O3tocbs5Q2hid5sx10JyKaJcw4ynTqsYzt5Vy8lI/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vd3d3Lm9w/aW5kaWEuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDI1LzA3/L1BhbGFtdS10d2lu/LWZvcnRzLXRvLWJl/LXJlc3RvcmVkXy1K/aGFya2hhbmQucG5n/P3Jlc2l6ZT02OTYs/Mzk4JnNzbD0x",
     "tagline":"Tiger Reserve & Fort",
     "attractions":[
                  {"title":"Palamu Fort","subtitle":"Historic fort","image":"https://imgs.search.brave.com/6r3O3tocbs5Q2hid5sx10JyKaJcw4ynTqsYzt5Vy8lI/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vd3d3Lm9w/aW5kaWEuY29tL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDI1LzA3/L1BhbGFtdS10d2lu/LWZvcnRzLXRvLWJl/LXJlc3RvcmVkXy1K/aGFya2hhbmQucG5n/P3Jlc2l6ZT02OTYs/Mzk4JnNzbD0x","desc":"Ruins within Palamu Tiger Reserve."},
         {"title":"Betla National Park","subtitle":"Diverse wildlife","image":"https://www.tourmyindia.com/states/jharkhand/images/betla-national-park1-1.jpg","desc":"Home to tigers, elephants, and various bird species."}
     ],
     "food":["Local dhokla","Chilka roti"], "handicrafts":["Tribal weaving"], "stays":["Forest cottages"]
    },
    {"name":"deoghar","display":"Deoghar", "slug":"deoghar",
     "image":"https://imgs.search.brave.com/ncSjoJ4bdvl0TD5G_uXmO_KCEbIckhrGdXsL9WrFpco/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zN2Fw/MS5zY2VuZTcuY29t/L2lzL2ltYWdlL2lu/Y3JlZGlibGVpbmRp/YS9iYWJhLWJhaWR5/YW5hdGgtZGhhbS1k/ZW9naGFyLW9kaXNo/YS10cmktaGVyby0x/P3FsdD04MiZ0cz0x/NzI3MTYzODU1Mzg3",
     "tagline":"Pilgrimage Hub",
     "attractions":[
         {"title":"Baidyanath Temple","subtitle":"Famous temple","image":"https://imgs.search.brave.com/ncSjoJ4bdvl0TD5G_uXmO_KCEbIckhrGdXsL9WrFpco/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9zN2Fw/MS5zY2VuZTcuY29t/L2lzL2ltYWdlL2lu/Y3JlZGlibGVpbmRp/YS9iYWJhLWJhaWR5/YW5hdGgtZGhhbS1k/ZW9naGFyLW9kaXNo/YS10cmktaGVyby0x/P3FsdD04MiZ0cz0x/NzI3MTYzODU1Mzg3","desc":"One of the 12 Jyotirlingas."},
         {"title":"Trikut Pahar","subtitle":"Hilltop pilgrimage","image":"https://deoghar.nic.in/wp-content/uploads/2023/02/Trikut-pahar-deoghar.jpg","desc":"Scenic hills with a ropeway and temples."}
     ],
     "food":["Sweets","Prasad dishes"], "handicrafts":["Temple crafts"], "stays":["Pilgrim lodges"]
    },
    {"name":"jamshedpur","display":"Jamshedpur", "slug":"jamshedpur",
     "image":"https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80",
     "tagline":"Steel City & Parks",
     "attractions":[
         {"title":"Jubilee Park","subtitle":"Urban park","image":"https://images.unsplash.com/photo-1502082553048-f009c37129b9?auto=format&fit=crop&w=800&q=80","desc":"Lush gardens and lake."},
         {"title":"Dalma Wildlife Sanctuary","subtitle":"Elephants and nature","image":"https://www.transindiatravels.com/wp-content/uploads/dalma-wildlife-sanctuary-jamshedpur.jpg","desc":"A dense forest sanctuary known for its elephant population."}
     ],
     "food":["Street food","Local cuisine"], "handicrafts":["Local crafts"], "stays":["Hotels","Apartments"]
    },
    {"name":"bokaro","display":"Bokaro", "slug":"bokaro",
     "image":"https://www.holidify.com/images/cmsuploads/compressed/Bokaro_Steel_City_20190211153131.jpg",
     "tagline":"Steel Capital",
     "attractions":[
         {"title":"Bokaro Steel Plant","subtitle":"Industrial giant","image":"https://www.bokarosteel.com/wp-content/uploads/2018/07/about-us-1.jpg","desc":"One of the largest steel plants in India."},
         {"title":"Garga Dam","subtitle":"Scenic reservoir","image":"https://www.holidify.com/images/cmsuploads/compressed/GargaDam_20190211153201.jpg","desc":"A popular picnic spot with serene views."}
     ],
     "food":["Litti Chokha","Dhuska"], "handicrafts":["Local crafts"], "stays":["Hotels","Guesthouses"]
    },
    {"name":"chatra","display":"Chatra", "slug":"chatra",
     "image":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Bhadrakali_Temple_Itkhori_Chatra.jpg/1024px-Bhadrakali_Temple_Itkhori_Chatra.jpg",
     "tagline":"Gateway to Jharkhand",
     "attractions":[
         {"title":"Bhadrakali Temple","subtitle":"Ancient temple complex","image":"https://chatra.nic.in/wp-content/uploads/2018/12/Bhadrakali-Itkhori.jpg","desc":"A confluence of Hinduism, Buddhism, and Jainism."},
         {"title":"Tamassin Falls","subtitle":"Mystical waterfall","image":"https://chatra.nic.in/wp-content/uploads/2018/12/Tama-sin.jpg","desc":"A scenic waterfall surrounded by lush greenery."}
     ],
     "food":["Local tribal cuisine","Sattu Paratha"], "handicrafts":["Bamboo crafts"], "stays":["Guesthouses","Lodges"]
    },
    {"name":"dhanbad","display":"Dhanbad", "slug":"dhanbad",
     "image":"https://www.dhanbadonline.in/city-guide/images/maithan-dam.jpg",
     "tagline":"The Coal Capital",
     "attractions":[
         {"title":"Maithon Dam","subtitle":"Hydropower project","image":"https://www.tourmyindia.com/states/jharkhand/images/maithon-dam1-1.jpg","desc":"A large dam on the Barakar River, popular for boating."},
         {"title":"Panchet Dam","subtitle":"Picturesque reservoir","image":"https://dhanbad.nic.in/wp-content/uploads/2023/04/2023040353-1.jpg","desc":"Known for its scenic beauty and picnic spots."}
     ],
     "food":["Litti Chokha","Thekua"], "handicrafts":["Coal souvenirs"], "stays":["Hotels","Resorts"]
    },
    {"name":"dumka","display":"Dumka", "slug":"dumka",
     "image":"https://dumka.nic.in/wp-content/uploads/2023/03/2023031133.jpg",
     "tagline":"Heart of Santhal Pargana",
     "attractions":[
         {"title":"Maluti Temples","subtitle":"Village of temples","image":"https://www.holidify.com/images/cmsuploads/compressed/Maluti_Temples_20190211153312.jpg","desc":"A unique village with 72 ancient terracotta temples."},
         {"title":"Masanjore Dam","subtitle":"Canada Dam","image":"https://www.tourmyindia.com/states/jharkhand/images/masanjore-dam1-1.jpg","desc":"A major dam on the Mayurakshi River, offering stunning views."}
     ],
     "food":["Local Santhali cuisine","Pitha"], "handicrafts":["Tribal art","Handlooms"], "stays":["Hotels","Guesthouses"]
    },
    {"name":"garhwa","display":"Garhwa", "slug":"garhwa",
     "image":"https://garhwa.nic.in/wp-content/uploads/2023/03/Sukhaldari-falls-Garhwa.jpg",
     "tagline":"Nature's Abode",
     "attractions":[
         {"title":"Sukhaldari Falls","subtitle":"Scenic waterfall","image":"https://media-cdn.tripadvisor.com/media/photo-s/1b/98/60/60/sukhaldari-falls.jpg","desc":"A beautiful waterfall on the Kanhar River."},
         {"title":"Parasdiha Falls","subtitle":"Picnic spot","image":"https://mapio.net/images-p/113835088.jpg","desc":"A popular spot for picnics and nature lovers."}
     ],
     "food":["Dhuska","Thekua"], "handicrafts":["Local crafts"], "stays":["Guesthouses"]
    },
    {"name":"giridih","display":"Giridih", "slug":"giridih",
     "image":"https://www.holidify.com/images/cmsuploads/compressed/Parasnath_Hills_20190211153421.jpg",
     "tagline":"Land of Hills",
     "attractions":[
         {"title":"Parasnath Hills","subtitle":"Jain pilgrimage site","image":"https://www.tourmyindia.com/states/jharkhand/images/parasnath-hills1-1.jpg","desc":"The highest peak in Jharkhand, a major Jain pilgrimage center."},
         {"title":"Usri Falls","subtitle":"Gushing waterfall","image":"https://giridih.nic.in/wp-content/uploads/2023/03/Usri-Falls-Giridih.jpg","desc":"A beautiful waterfall on the Usri River."}
     ],
     "food":["Litti Chokha","Pua"], "handicrafts":["Stone carvings"], "stays":["Dharamshalas","Hotels"]
    },
    {"name":"godda","display":"Godda", "slug":"godda",
     "image":"https://godda.nic.in/wp-content/uploads/2023/03/Yogini-shakti-peeth-godda.jpg",
     "tagline":"Spiritual Land",
     "attractions":[
         {"title":"Yogini Shakti Peeth","subtitle":"Ancient temple","image":"https://www.telegraphindia.com/unsafe/1200x800/smart/static.telegraphindia.com/derivative/THE_TELEGRAPH/1813220/16X9/imagec83b1f19-d2b7-404b-89c0-a34a63a3255c.jpg","desc":"An ancient temple dedicated to Goddess Sati."},
         {"title":"Sundar Dam","subtitle":"Reservoir","image":"https://godda.nic.in/wp-content/uploads/2023/03/Sunder-Dam-godda.jpg","desc":"A large dam and reservoir, ideal for picnics."}
     ],
     "food":["Local cuisine","Sweets"], "handicrafts":["Local crafts"], "stays":["Guesthouses"]
    },
    {"name":"gumla","display":"Gumla", "slug":"gumla",
     "image":"https://gumla.nic.in/wp-content/uploads/2023/04/2023040338.jpg",
     "tagline":"Tribal Heritage",
     "attractions":[
         {"title":"Nagfeni Temple","subtitle":"Snake-hood rock","image":"https://gumla.nic.in/wp-content/uploads/2023/04/2023040340.jpg","desc":"A temple known for its natural rock formation resembling a snake's hood."},
         {"title":"Sadni Falls","subtitle":"Cascading beauty","image":"https://gumla.nic.in/wp-content/uploads/2023/04/2023040343.jpg","desc":"A beautiful waterfall with a significant drop."}
     ],
     "food":["Tribal dishes","Handia"], "handicrafts":["Bamboo products"], "stays":["Lodges"]
    },
    {"name":"hazaribagh","display":"Hazaribagh", "slug":"hazaribagh",
     "image":"https://hazaribag.nic.in/wp-content/uploads/2023/03/Canary-Hill-Hazaribag.jpg",
     "tagline":"City of a Thousand Gardens",
     "attractions":[
         {"title":"Hazaribagh National Park","subtitle":"Wildlife sanctuary","image":"https://www.tourmyindia.com/states/jharkhand/images/hazaribagh-wildlife-sanctuary1-1.jpg","desc":"Home to various species of flora and fauna."},
         {"title":"Canary Hill","subtitle":"Panoramic views","image":"https://www.holidify.com/images/cmsuploads/compressed/CanaryHills_20190211153512.jpg","desc":"A hill with a watchtower offering panoramic views of the city."}
     ],
     "food":["Local delicacies","Sweets"], "handicrafts":["Wooden toys"], "stays":["Hotels","Resorts"]
    },
    {"name":"jamtara","display":"Jamtara", "slug":"jamtara",
     "image":"https://jamtara.nic.in/wp-content/uploads/2023/03/Parwat-Vihar-Park-Jamtara.jpg",
     "tagline":"Land of Snakes",
     "attractions":[
         {"title":"Parwat Vihar Park","subtitle":"Recreational park","image":"https://jamtara.nic.in/wp-content/uploads/2023/03/Parwat-Vihar-Park-Jamtara.jpg","desc":"A park located on a hillock, offering nice views."},
         {"title":"Ladhana Dam","subtitle":"Scenic spot","image":"https://jamtara.nic.in/wp-content/uploads/2023/03/Ladhana-Dam-Jamtara.jpg","desc":"A serene dam and reservoir."}
     ],
     "food":["Local food","Sweets"], "handicrafts":["Local crafts"], "stays":["Guesthouses"]
    },
    {"name":"khunti","display":"Khunti", "slug":"khunti",
     "image":"https://khunti.nic.in/wp-content/uploads/2023/03/Panchghagh-falls-khunti.jpg",
     "tagline":"Birthplace of Birsa Munda",
     "attractions":[
         {"title":"Panchghagh Falls","subtitle":"Five waterfalls","image":"https://www.holidify.com/images/cmsuploads/compressed/Panchghagh_Falls_20190211153601.jpg","desc":"A collective of five waterfalls, creating a stunning sight."},
         {"title":"Ulihatu","subtitle":"Birthplace of a legend","image":"https://khunti.nic.in/wp-content/uploads/2023/03/Ulihatu-khunti.jpg","desc":"The birthplace of the tribal freedom fighter, Birsa Munda."}
     ],
     "food":["Tribal cuisine","Rice beer"], "handicrafts":["Dokra art"], "stays":["Lodges"]
    },
    {"name":"koderma","display":"Koderma", "slug":"koderma",
     "image":"https://koderma.nic.in/wp-content/uploads/2023/03/Tilaiya-Dam-Koderma.jpg",
     "tagline":"Mica Capital of India",
     "attractions":[
         {"title":"Tilaiya Dam","subtitle":"First dam of DVC","image":"https://www.tourmyindia.com/states/jharkhand/images/tilaiya-dam1-1.jpg","desc":"The first dam and hydro-electric power station constructed by the Damodar Valley Corporation."},
         {"title":"Petro Falls","subtitle":"Waterfall","image":"https://koderma.nic.in/wp-content/uploads/2023/03/Petro-Falls-koderma.jpg","desc":"A beautiful waterfall in a serene environment."}
     ],
     "food":["Local food","Til Barfi"], "handicrafts":["Mica products"], "stays":["Hotels","Guesthouses"]
    },
    {"name":"latehar","display":"Latehar", "slug":"latehar",
     "image":"https://latehar.nic.in/wp-content/uploads/2023/03/Netarhat-Latehar.jpg",
     "tagline":"Queen of Chotanagpur",
     "attractions":[
         {"title":"Netarhat","subtitle":"Hill station","image":"https://www.holidify.com/images/cmsuploads/compressed/Netarhat_20190211153652.jpg","desc":"A popular hill station known for its beautiful sunrise and sunset views."},
         {"title":"Lodh Falls","subtitle":"Highest waterfall in Jharkhand","image":"https://www.tourmyindia.com/states/jharkhand/images/lodh-falls1-1.jpg","desc":"The highest waterfall in Jharkhand, with a drop of 143 meters."}
     ],
     "food":["Local cuisine","Fruits"], "handicrafts":["Bamboo crafts"], "stays":["Hotels","Resorts"]
    },
    {"name":"lohardaga","display":"Lohardaga", "slug":"lohardaga",
     "image":"https://lohardaga.nic.in/wp-content/uploads/2023/04/2023040350.jpg",
     "tagline":"Land of Bauxite",
     "attractions":[
         {"title":"Lawapani Falls","subtitle":"Waterfall","image":"https://lohardaga.nic.in/wp-content/uploads/2023/04/2023040350.jpg","desc":"A scenic waterfall in the midst of nature."},
         {"title":"Kekrang Falls","subtitle":"Waterfall","image":"https://lohardaga.nic.in/wp-content/uploads/2023/04/2023040349.jpg","desc":"Another beautiful waterfall in the district."}
     ],
     "food":["Local food","Dhuska"], "handicrafts":["Local crafts"], "stays":["Guesthouses"]
    },
    {"name":"pakur","display":"Pakur", "slug":"pakur",
     "image":"https://pakur.nic.in/wp-content/uploads/2023/03/Sidhhu-Kanhu-Park-Pakur.jpg",
     "tagline":"Land of Black Stone",
     "attractions":[
         {"title":"Sidhhu Kanhu Park","subtitle":"Recreational park","image":"https://pakur.nic.in/wp-content/uploads/2023/03/Sidhhu-Kanhu-Park-Pakur.jpg","desc":"A park dedicated to the tribal heroes Sidhu and Kanhu Murmu."},
         {"title":"Martello Tower","subtitle":"Historical tower","image":"https://pakur.nic.in/wp-content/uploads/2023/03/Martello-Tower-Pakur.jpg","desc":"A historical tower built by the British."}
     ],
     "food":["Local cuisine","Sweets"], "handicrafts":["Stone crafts"], "stays":["Hotels"]
    },
    {"name":"ramgarh","display":"Ramgarh", "slug":"ramgarh",
     "image":"https://ramgarh.nic.in/wp-content/uploads/2023/03/Patratu-Valley-Ramgarh.jpg",
     "tagline":"Gateway to Chotanagpur",
     "attractions":[
         {"title":"Patratu Valley","subtitle":"Winding roads and views","image":"https://www.holidify.com/images/cmsuploads/compressed/Patratu_Valley_20190211153742.jpg","desc":"Famous for its scenic winding roads and the Patratu Dam."},
         {"title":"Rajrappa Temple","subtitle":"Chhinnamasta Temple","image":"https://www.tourmyindia.com/states/jharkhand/images/rajrappa-temple1-1.jpg","desc":"A famous temple dedicated to Goddess Chhinnamasta, located at the confluence of two rivers."}
     ],
     "food":["Local food","Snacks"], "handicrafts":["Local crafts"], "stays":["Hotels","Resorts"]
    },
    {"name":"sahibganj","display":"Sahibganj", "slug":"sahibganj",
     "image":"https://sahibganj.nic.in/wp-content/uploads/2023/03/Moti-Jharna-sahibganj.jpg",
     "tagline":"Ganga's Gateway to Jharkhand",
     "attractions":[
         {"title":"Moti Jharna","subtitle":"Waterfall","image":"https://sahibganj.nic.in/wp-content/uploads/2023/03/Moti-Jharna-sahibganj.jpg","desc":"A beautiful waterfall in the Rajmahal hills."},
         {"title":"Udhwa Bird Sanctuary","subtitle":"Bird watcher's paradise","image":"https://www.tourmyindia.com/states/jharkhand/images/udhwa-lake-bird-sanctuary1-1.jpg","desc":"A bird sanctuary that attracts migratory birds from Siberia and Europe."}
     ],
     "food":["Fish curry","Sweets"], "handicrafts":["Terracotta toys"], "stays":["Hotels"]
    },
    {"name":"seraikela kharsawan","display":"Seraikela Kharsawan", "slug":"seraikela-kharsawan",
     "image":"https://seraikela-kharsawan.nic.in/wp-content/uploads/2023/04/2023040356.jpg",
     "tagline":"Land of Chhau Dance",
     "attractions":[
         {"title":"Chhau Dance","subtitle":"Traditional dance form","image":"https://www.unesco.org/new/fileadmin/MULTIMEDIA/HQ/CLT/images/Chhau_dance_India640x420.jpg","desc":"The district is famous for the Seraikela style of Chhau dance."},
         {"title":"Palna Dam","subtitle":"Reservoir","image":"https://seraikela-kharsawan.nic.in/wp-content/uploads/2023/04/2023040356.jpg","desc":"A scenic dam and reservoir."}
     ],
     "food":["Local cuisine","Arsa Roti"], "handicrafts":["Chhau masks"], "stays":["Guesthouses"]
    },
    {"name":"simdega","display":"Simdega", "slug":"simdega",
     "image":"https://simdega.nic.in/wp-content/uploads/2023/03/Kela-Ghagh-Dam-Simdega.jpg",
     "tagline":"Cradle of Hockey",
     "attractions":[
         {"title":"Kela Ghagh Dam","subtitle":"Dam and park","image":"https://simdega.nic.in/wp-content/uploads/2023/03/Kela-Ghagh-Dam-Simdega.jpg","desc":"A dam with a beautiful park, popular for picnics."},
         {"title":"Ram Rekha Dham","subtitle":"Pilgrimage site","image":"https://simdega.nic.in/wp-content/uploads/2023/03/Ram-Rekha-Dham-Simdega.jpg","desc":"A pilgrimage site where Lord Rama is believed to have stayed during his exile."}
     ],
     "food":["Local food","Dhuska"], "handicrafts":["Local crafts"], "stays":["Guesthouses"]
    },
    {"name":"west singhbhum","display":"West Singhbhum", "slug":"west-singhbhum",
     "image":"https://westsinghbhum.nic.in/wp-content/uploads/2023/03/Hirni-Falls-West-Singhbhum.jpg",
     "tagline":"Land of Iron Ore",
     "attractions":[
         {"title":"Hirni Falls","subtitle":"Waterfall","image":"https://westsinghbhum.nic.in/wp-content/uploads/2023/03/Hirni-Falls-West-Singhbhum.jpg","desc":"A scenic waterfall in a forested area."},
         {"title":"Saranda Forest","subtitle":"Asia's largest Sal forest","image":"https://www.tourmyindia.com/states/jharkhand/images/saranda-forest1-1.jpg","desc":"Known as the 'land of seven hundred hills', it is Asia's largest Sal forest."}
     ],
     "food":["Tribal cuisine","Local vegetables"], "handicrafts":["Iron crafts"], "stays":["Forest rest houses"]
    }
]

# Sample data for Admin Dashboard
DUMMY_VISITS = {
    "Ranchi": 1250, "Deoghar": 980, "Jamshedpur": 750, "Hazaribagh": 620,
    "Palamu": 450, "Netarhat": 880, "Bokaro": 320, "Giridih": 510,
}

DUMMY_FEEDBACK = [
    {
        "user": "tourist123",
        "rating": 4,
        "comment": "The waterfalls in Ranchi were breathtaking, but the roads leading to them could be better maintained. Also, more signages would be helpful.",
        "category": "Infrastructure"
    },
    {
        "user": "explorer_jane",
        "rating": 5,
        "comment": "Loved the cultural experience in Deoghar. The temple was serene. I would suggest promoting local handicrafts more actively near tourist spots.",
        "category": "Culture & Shopping"
    },
    {
        "user": "wildlife_bob",
        "rating": 3,
        "comment": "Betla National Park was a good experience, but we couldn't spot many animals. Maybe guided safaris could be better organized.",
        "category": "Adventure & Wildlife"
    },
    {
        "user": "foodie_sara",
        "rating": 5,
        "comment": "The local cuisine is amazing! Dhuska and Litti Chokha are a must-try. More food stalls near major attractions would be great.",
        "category": "Food & Beverage"
    }
]

AI_SUGGESTIONS = {
    "summary": "Overall tourist sentiment is positive, with high appreciation for natural beauty and cultural sites. Key areas for improvement are infrastructure (roads, signage) and better organization of services like safaris. There is a strong interest in local culture, handicrafts, and cuisine, indicating a growth opportunity.",
    "actionable_insights": [
        "Prioritize road repairs and install clear signages for routes leading to major waterfalls and parks.",
        "Develop a program to promote and sell local handicrafts at dedicated kiosks near tourist hubs.",
        "Review and enhance the guided safari packages in national parks to improve wildlife sighting opportunities.",
        "Increase the availability of authentic local food vendors at popular tourist locations."
    ],
    "sentiment_by_category": {
        "Natural Sites": "Very Positive",
        "Cultural/Religious Sites": "Very Positive",
        "Infrastructure": "Needs Improvement",
        "Services (Guides, Safaris)": "Mixed",
        "Food & Shopping": "Positive"
    }
}

def index(request):
    context = {
        "carousel_images": CAROUSEL, 
        "districts": DISTRICTS,
        "experiences": EXPERIENCES
    }
    return render(request, 'tourism/index.html', context)

def district_view(request, slug):
    d = next((x for x in DISTRICTS if x["slug"] == slug), None)
    if not d:
        # simple fallback: try lowercase match of slug parameter (for searchRedirect)
        d = next((x for x in DISTRICTS if x["name"] == slug.lower()), None)
    if not d:
        raise Http404("District not found (demo)")
    return render(request, 'tourism/district.html', {"district": d})

def dashboard(request):
    top = [{"name":"Ranchi", "visits":420},{"name":"Deoghar","visits":320},{"name":"Palamu","visits":150}]
    return render(request, 'tourism/dashboard.html', {"top_districts":top})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tourism:user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'tourism/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('tourism:admin_dashboard')
            return redirect('tourism:user_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'tourism/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('tourism:index')
    # Redirect GET requests to home or show a confirmation page
    return redirect('tourism:index')

@login_required
def user_dashboard(request):
    # This view will be for regular logged-in users.
    # Dummy data for User Dashboard
    DUMMY_PLANNED_TRIPS = [
        {"name": "Netarhat", "date": "2025-10-15", "status": "Upcoming"},
        {"name": "Parasnath Hills", "date": "2025-11-20", "status": "Upcoming"},
    ]

    DUMMY_EXPLORED_PLACES = [
        {"name": "Hundru Falls", "date": "2025-07-22", "rating": 5},
        {"name": "Jubilee Park", "date": "2025-05-10", "rating": 4},
        {"name": "Baidyanath Temple", "date": "2025-02-18", "rating": 5},
    ]
    
    context = {
        "planned_trips": DUMMY_PLANNED_TRIPS,
        "explored_places": DUMMY_EXPLORED_PLACES,
    }
    return render(request, 'tourism/user_dashboard.html', context)


@login_required
def sos_alert(request):
    # Later, you can integrate SMS/email/notification here
    return HttpResponse("🚨 SOS Alert Triggered!")

import json

# ... (previous code) ...

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Sort districts by visits in descending order
    sorted_visits = sorted(DUMMY_VISITS.items(), key=lambda x: x[1], reverse=True)
    
    # Prepare data for charts
    visit_labels = [item[0] for item in sorted_visits]
    visit_data = [item[1] for item in sorted_visits]

    # Convert sentiment text to numerical data for charting
    sentiment_mapping = {"Very Positive": 2, "Positive": 1, "Mixed": 0, "Needs Improvement": -1}
    place_type_labels = list(AI_SUGGESTIONS['sentiment_by_category'].keys())
    place_type_data = [sentiment_mapping[s] for s in AI_SUGGESTIONS['sentiment_by_category'].values()]

    context = {
        'total_tourists': sum(DUMMY_VISITS.values()),
        'most_visited_places': sorted_visits,
        'feedback_list': DUMMY_FEEDBACK,
        'ai_suggestions': AI_SUGGESTIONS,
        'visit_labels': json.dumps(visit_labels),
        'visit_data': json.dumps(visit_data),
        'place_type_labels': json.dumps(place_type_labels),
        'place_type_data': json.dumps(place_type_data),
    }
    return render(request, 'tourism/admin_dashboard.html', context)

def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                return redirect('tourism:admin_dashboard')
            else:
                # Optional: Add a message for non-admin users trying to log in here
                pass
    else:
        form = AuthenticationForm()
    return render(request, 'tourism/admin_login.html', {'form': form})



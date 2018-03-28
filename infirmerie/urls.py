# This file is part of Appyschool.
#
# Appyschool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# Appyschool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Appyschool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Appyschool.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='infirmerie'),
    url(r'^get_malades$', views.get_malades, name='get_malades'),
    url(r'^ajouter_malade$', views.ajouter_malade, name='ajouter_malade'),
    url(r'^encoder_sortie/(?P<passageId>[0-9]+)$', views.encoder_sortie, name='encoder_sortie'),
    url(r'^get_entries/$', views.get_entries, name='get_entries'),
    url(r'^get_entries/(?P<ens>\w+)/(?P<column>\w+)/$', views.get_entries, name='get_entries'),
]

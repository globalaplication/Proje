#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi, os, copy
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio, Gdk
from gi.repository import GdkPixbuf, GLib
from gi.repository import Pango
import subprocess, platform
from cc import CopyCut
HOME = os.environ['HOME']
PlacesSource = HOME+'/.config/_filemanager_py_mt_nr.places'
DefaultPlaces = HOME+'/.config/user-dirs.dirs'
LastSelect = HOME+'/.config/_filemanager_py_mt_nr.star'
BlueToothSelectFiles = HOME+'/config/SendData.blue'
filedict = {}
SelectDebFiles = []
pdict = {}
pdict['Diskler'] = {'path':'/media', 'icon':'gtk-home', 'main':True}
pdict['Rash'] = {'path':HOME+'/.local/share/Trash/files/', 'icon':'gtk-quit', 'main':True}
pdict['Ev'] = {'path':HOME, 'icon':'gtk-home', 'main':True}
pdict['Root'] = {'path':'/', 'icon':'gtk-home', 'main':True}

def ConfigDeletePlaces(string, NewConfigData=''):
    with open(PlacesSource) as delete:
        test = delete.read()
    for j in test.splitlines():
        if j.startswith(string) is True:
            continue
        NewConfigData = NewConfigData + j + '\n'
    with open(PlacesSource, 'w') as places:
        places.write(NewConfigData)
def TempRead():
    with open(LastSelect) as temp:
        star = temp.read().replace('\n', '')
    return star
def TempWrite(path):
    with open(LastSelect, 'w') as temp:
        temp.write(path)
def ConfigAddPlaces(keys, value, icon, main):
    with open(PlacesSource) as oku:
        test = oku.read()
    if test.find(keys+',') is -1:
        with open(PlacesSource, 'a') as places:
            places.write(keys+','+value+','+icon+','+str(main)+'\n')
def LoadPlaces():
    with open(DefaultPlaces) as pla:
        places = pla.read().splitlines()
    places = [places.replace('"','').split('/')[-1] for places in places if places.startswith('#') is False]
    for add in places:
        ConfigAddPlaces(HOME+'/'+add, add, 'gtk-home', True)
    with open(PlacesSource) as pla:
        places = pla.read().splitlines()
    for add in places:
        if len(add.split(',')[1]) is not 0:
            pdict[add.split(',')[1]] = {'path':add.split(',')[0], 
            'icon':add.split(',')[2], 
                                        'main':add.split(',')[3]}
    return pdict


class FileOptions(Gtk.FileChooserDialog):
    SupportIconList = ['.png']
    def on_folder_clicked(self, widget, data):
        dialog = Gtk.FileChooserDialog("Lütfen Klasör Seç", self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Seçildi: " + dialog.get_filename(), data)
            data.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass
    def make(self, DesktopCheckButton):
        DebMakeString = ''
        DesktopMakeString = ''
        MainPath = SelectDebFiles[-1]
        DebDirs = os.path.split(MainPath)[1]
        DebMakeFolder = SelectDebFiles[-1]+'/'+DebDirs+'/DEBIAN'
        if os.path.isdir(DebMakeFolder) is False:
            os.makedirs(DebMakeFolder)
        os.system('touch '+DebMakeFolder+'/control')
        for DebMake in [self.Entry1,self.Entry2,self.Entry3,self.Entry4,self.Entry5,self.Entry6]:
            if os.path.isdir(MainPath+'/'+DebDirs+'/'+DebMake.get_text()) is False:
                os.makedirs(MainPath+'/'+DebDirs+'/'+DebMake.get_text())
        for DebMake in zip([self.File1,self.File2,self.File3,self.File4,self.File5,self.File6],
                [self.Entry1,self.Entry2,self.Entry3,self.Entry4,self.Entry5,self.Entry6]):
            if ( len(DebMake[0].get_text()) is not 0):
                os.system('cp -avr '+MainPath+'/'+DebMake[0].get_text()+' '+MainPath+'/'+DebDirs+DebMake[1].get_text())
        for DebMake in zip([self.CpuEntry], ['Architecture:']):
            if (DebMake[0].get_active_text() is not None):
                DebMakeString = DebMakeString + DebMake[1]+chr(32)+DebMake[0].get_active_text() +'\n'
        #for DebMake in zip(['Version:', 'Name:', 'Encoding:', 'Comment:', 'Path:', 'Exec:', 'Icon:', 'Terminal:', 'Type:', 'Categories:'],
        #                    [self.VersionEntry, self.PackageEntry, 'Utf-8', self.DescriptionEntry]):
        #    if (DebMake[0] == 'Encoding:'):
        #        DesktopMakeString = DesktopMakeString + DebMake[0] +' '+  DebMake[1] + '\n'
        #        continue
        #    DesktopMakeString = DesktopMakeString + DebMake[0] +' '+  DebMake[1].get_text() + '\n'
        #print DesktopMakeString
        for DebMake in zip([self.PackageEntry, self.VersionEntry, self.SectionEntry, 
                            self.PriorityEntry, self.ContactEntry, 
                            self.DescriptionEntry], 
                           ['Package:', 'Version:', 'Section:', 'Priority:', 
                            'Maintainer:', 'Description:']):
            DebMakeString = DebMakeString + DebMake[1]+chr(32)+DebMake[0].get_text() +'\n'
            with open(DebMakeFolder+'/control', 'w') as make:
                make.write(DebMakeString)
        if (self.StartUpCheckButton.get_active() is True):
            print 'Başlangıçta Çalış'
        if (self.DesktopCheckButton.get_active() is True):
            print 'Desktop Kısayol Oluştur'
            ApplicationsPath = '/usr/share/applications'
            if os.path.isdir(MainPath+'/'+DebDirs+ApplicationsPath) is False:
                os.makedirs(MainPath+'/'+DebDirs+ApplicationsPath)
        #os.system('dpkg-deb --build '+ SelectDebFiles[-1]+'/'+DebDirs)

    def __init__(self, BetaApp):

        self.DebMakeWindow = Gtk.Window()
        self.DebMakeWindow.set_default_size(300, 300)
        self.DebMakeWindow.set_border_width(11)

        self.Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.DebMakeWindow.add(self.Box)
        self.ListBox = Gtk.ListBox()
        self.ListBox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.Box.pack_start(self.ListBox, True, True, 0)



        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.ExecLabel = Gtk.Label("Exec", xalign=0)
        self.ExecEntry = Gtk.Entry()
        self.ExecEntry.set_sensitive(False)
        self.ExecEntry.set_text('Python')
        hbox.pack_start(self.ExecLabel, True, True, 0)
        hbox.pack_start(self.ExecEntry, False, True, 0)
        self.ListBox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.PackageLabel = Gtk.Label("Paket", xalign=0)
        self.PackageEntry = Gtk.Entry()
        self.PackageEntry.set_sensitive(False)
        self.PackageEntry.set_text(os.path.split(SelectDebFiles[-1])[1])
        hbox.pack_start(self.PackageLabel, True, True, 0)
        hbox.pack_start(self.PackageEntry, False, True, 0)
        self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.VersionLabel = Gtk.Label("Versiyon", xalign=0)
        self.VersionEntry = Gtk.Entry()
        self.VersionEntry.set_text('0.1')
        hbox.pack_start(self.VersionLabel, True, True, 0)
        hbox.pack_start(self.VersionEntry, False, True, 0)
        self.ListBox.add(row)



        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.CategoriesLabel = Gtk.Label("Kategori", xalign=0)
        self.CategoriesComboBoxText = Gtk.ComboBoxText()
        self.CategoriesComboBoxText.insert(0, "0", "GNOME")
        self.CategoriesComboBoxText.insert(1, "1", "GTK")
        self.CategoriesComboBoxText.insert(2, "2", "Graphics")
        self.CategoriesComboBoxText.insert(3, "3", "Office")
        self.CategoriesComboBoxText.insert(4, "4", "Settings")
        self.CategoriesComboBoxText.insert(5, "5", "System")
        self.CategoriesComboBoxText.insert(6, "6", "Utility")
        self.CategoriesComboBoxText.insert(7, "7", "Development")
        self.CategoriesComboBoxText.insert(8, "8", "Education")
        self.CategoriesComboBoxText.insert(9, "9", "Utility")
        self.CategoriesComboBoxText.insert(10, "10", "Game") 
        self.CategoriesComboBoxText.set_active(7)    
        self.CategoriesComboBoxText.set_sensitive(True)
        hbox.pack_start(self.CategoriesLabel, True, True, 0)
        hbox.pack_start(self.CategoriesComboBoxText, False, True, 0)
        self.ListBox.add(row)



        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.SectionLabel = Gtk.Label("Section", xalign=0)
        self.SectionEntry = Gtk.Entry()
        self.SectionEntry.set_text('base')
        hbox.pack_start(self.SectionLabel, True, True, 0)
        hbox.pack_start(self.SectionEntry, False, True, 0)
        #self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.PriorityLabel = Gtk.Label("Priority", xalign=0)
        self.PriorityEntry = Gtk.Entry()
        self.PriorityEntry.set_text('optional')
        hbox.pack_start(self.PriorityLabel, True, True, 0)
        hbox.pack_start(self.PriorityEntry, False, True, 0)
        #self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.ContactLabel = Gtk.Label("İletişim", xalign=0)
        self.ContactEntry = Gtk.Entry()
        self.ContactEntry.set_text('@glabalapplication')
        hbox.pack_start(self.ContactLabel, True, True, 0)
        hbox.pack_start(self.ContactEntry, False, True, 0)
        self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.DescriptionLabel = Gtk.Label("Açıklama", xalign=0)
        self.DescriptionEntry = Gtk.Entry()
        self.DescriptionEntry.set_text('Masaüstü Uygulaması')
        hbox.pack_start(self.DescriptionLabel, True, True, 0)
        hbox.pack_start(self.DescriptionEntry, False, True, 0)
        self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.CpuLabel = Gtk.Label("İslemci Mimarisi", xalign=0)
        self.CpuEntry = Gtk.ComboBoxText()
        self.CpuEntry.insert(0, "0", "i386")
        self.CpuEntry.insert(1, "1", "i684")
        self.CpuEntry.set_sensitive(True)
        self.CpuEntry.set_active(0)   
        #self.CpuEntry.set_text('i386') #'platform.machine()' 'amd64'
        hbox.pack_start(self.CpuLabel, True, True, 0)
        hbox.pack_start(self.CpuEntry, False, True, 0)
        self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.StartUpLabel = Gtk.Label("Başlangıçta Çalıştır", xalign=0)
        self.StartUpCheckButton = Gtk.CheckButton()
        hbox.pack_start(self.StartUpLabel, True, True, 0)
        hbox.pack_start(self.StartUpCheckButton, False, True, 0)
        self.ListBox.add(row)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.DesktopLabel = Gtk.Label("Desktop Kısayol", xalign=0)
        self.DesktopCheckButton = Gtk.CheckButton()
        hbox.pack_start(self.DesktopLabel, True, True, 0)
        hbox.pack_start(self.DesktopCheckButton, False, True, 0)
        self.ListBox.add(row)
        self.ListBox2 = Gtk.ListBox()
        self.ListBox2.set_selection_mode(Gtk.SelectionMode.NONE)
        self.Box.pack_start(self.ListBox2, True, True, 0)
        self.File1 = Gtk.Label(xalign=0)
        self.Entry1 = Gtk.Entry()
        self.Load1 = Gtk.Button("")
        self.Load1.connect("clicked", self.on_folder_clicked, self.Entry1)
        self.File2 = Gtk.Label(xalign=0)
        self.Entry2 = Gtk.Entry()
        self.Load2 = Gtk.Button("")
        self.Load2.connect("clicked", self.on_folder_clicked, self.Entry2)
        self.File3 = Gtk.Label(xalign=0)
        self.Entry3 = Gtk.Entry()
        self.Load3 = Gtk.Button("")
        self.Load3.connect("clicked", self.on_folder_clicked, self.Entry3)
        self.File4 = Gtk.Label(xalign=0)
        self.Entry4 = Gtk.Entry()
        self.Load4 = Gtk.Button("")
        self.Load4.connect("clicked", self.on_folder_clicked, self.Entry4)
        self.File5 = Gtk.Label(xalign=0)
        self.Entry5 = Gtk.Entry()
        self.Load5 = Gtk.Button("")
        self.Load5.connect("clicked", self.on_folder_clicked, self.Entry5)
        self.File6 = Gtk.Label(xalign=0)
        self.Entry6 = Gtk.Entry()
        self.Load6 = Gtk.Button("")
        self.Load6.connect("clicked", self.on_folder_clicked, self.Entry6)
        for make in zip([self.File1, self.File2, self.File3, 
                        self.File4, self.File5, self.File6],
                        [self.Entry1, self.Entry2, self.Entry3, 
                        self.Entry4, self.Entry5, self.Entry6],
                        SelectDebFiles[0:-1], 
                        [self.Load1, self.Load2, self.Load3, 
                        self.Load4, 
                        self.Load5, self.Load6]):
            row = Gtk.ListBoxRow()
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            row.add(hbox)
            make[0].set_text(os.path.split(make[2])[1])
            if (make[2][make[2].find('.'):] == '.py' or make[2][make[2].find('.'):] == '.pyc'):
                make[1].set_text('/usr/local/bin')
            if (make[2][make[2].find('.'):] in self.SupportIconList):
                self.DesktopCheckButton.set_active(1)
            hbox.pack_start(make[0], True, True, 0)
            hbox.pack_start(make[1], False, True, 0)
            hbox.pack_start(make[3], False, True, 0)
            self.ListBox2.add(row)
        self.ListBox3 = Gtk.ListBox()
        self.ListBox3.set_selection_mode(Gtk.SelectionMode.NONE)
        self.Box.pack_start(self.ListBox3, True, True, 0)
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(hbox)
        self.DesktopLabel = Gtk.Label("Deb Paket Dosyası", xalign=0)
        self.DesktopMakeButton = Gtk.Button('Oluştur')
        self.DesktopMakeButton.connect('clicked', self.make)
        hbox.pack_start(self.DesktopLabel, True, True, 0)
        hbox.pack_start(self.DesktopMakeButton, False, True, 0)
        self.ListBox3.add(row)
        self.DebMakeWindow.show_all()

class BetaFileManager(Gtk.Window):
    (COL_PATH, FILENAME, FILEICON, COL_IS_DIRECTORY,
        NUM_COLS) = range(5)
    Path = TempRead()
    IconWidth = 60
    ArrayNextBack, CountNextBack = [Path], 1
    state = False
    SelectPlacesItem = 0
    CtrL = False
    SelectPlacesItemIter = 0
    SelectPlacesItemChangePdict = {}
    DefaultFolder = 'Klasör'
    IconViewSelectedItem = []
    CountFolder = 0
    CountText = 0
    CountHideFile = 0
    SelectIconViewIsdir = False
    ExtendSelectIconViewIndex = []
    ExtendSelectIconViewFile = []
    RashPath = HOME+'/.local/share/Trash/files/'
    IcinViewSelectOptions = ''
    IconViewDialogChangeGetText = []
    IconViewSelectIndex = -1
    def __init__(self, BetaApp):
        self.window = Gtk.Window()
        self.window.set_default_size(960, 600)
        self.window.connect('destroy', Gtk.main_quit)
        #self.paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.menu = Gtk.Menu()
        MenuKonumlarSil = Gtk.MenuItem("Sil")
        MenuKonumlarSil.connect("activate", self.PlacesTreeViewFonksiyon, 'Sil')
        MenuKonumlarDegistir = Gtk.MenuItem("Yeniden Adlandır")
        MenuKonumlarDegistir.connect("activate", self.PlacesTreeViewFonksiyon, 'Yeniden Adlandır')
        self.menu.append(MenuKonumlarDegistir)
        self.menu.append(MenuKonumlarSil)
        self.menu.show_all()

        self.MenuIconView = Gtk.Menu()

        self.MenuIconViewGdeb = Gtk.MenuItem("Gdeb")
        self.MenuIconViewGdeb.connect("activate", self.IconViewFonksiyon, 'Gdeb')

        self.MenuIconViewSendBlue = Gtk.MenuItem("BlueTooth ile Gönder")
        self.MenuIconViewSendBlue.connect("activate", self.IconViewFonksiyon, 'BlueTooth ile Gönder')

        self.MenuIconViewCopy = Gtk.MenuItem("Kopyala")
        self.MenuIconViewCopy.connect("activate", self.IconViewFonksiyon, 'Kopyala')
        #self.MenuIconViewCopy.connect("activate", self.on_folder_clicked)

        self.MenuIconViewCut = Gtk.MenuItem("Taşı")
        self.MenuIconViewCut.connect("activate", self.IconViewFonksiyon, 'Taşı')
        self.MenuIconViewPaste = Gtk.MenuItem("Yapıştır")
        self.MenuIconViewPaste.connect("activate", self.IconViewFonksiyon, 'Yapıştır')
        self.MenuIconViewYeniKlasor = Gtk.MenuItem("Yeni Klasör")
        self.MenuIconViewYeniKlasor.connect("activate", self.IconViewFonksiyon, 'Yeni Klasör')
        self.MenuIconViewDelete = Gtk.MenuItem("Sil")
        self.MenuIconViewDelete.connect("activate", self.IconViewFonksiyon, 'Sil')
        self.MenuIconViewCopeTasi = Gtk.MenuItem("Çöp Kutusuna Taşı")
        self.MenuIconViewCopeTasi.connect("activate", self.IconViewFonksiyon, 'Çöp Kutusuna Taşı')
        self.MenuIconViewFolderAddPlaces = Gtk.MenuItem("Konuma Ekle ")
        self.MenuIconViewFolderAddPlaces.connect("activate", self.IconViewFonksiyon, 'Konuma Ekle')
        self.MenuIconViewChanged = Gtk.MenuItem("Yeniden Adlandır")
        self.MenuIconViewChanged.connect("activate", self.IconViewFonksiyon, 'Yeniden Adlandır')

        self.MenuIconView.append(self.MenuIconViewGdeb)
        self.MenuIconView.append(self.MenuIconViewSendBlue)
        self.MenuIconView.append(self.MenuIconViewCopy)
        self.MenuIconView.append(self.MenuIconViewCut)
        self.MenuIconView.append(self.MenuIconViewPaste)
        self.MenuIconView.append(self.MenuIconViewFolderAddPlaces)
        self.MenuIconView.append(self.MenuIconViewYeniKlasor)
        self.MenuIconView.append(self.MenuIconViewDelete)
        self.MenuIconView.append(self.MenuIconViewCopeTasi)
        self.MenuIconView.append(self.MenuIconViewChanged)
        self.MenuIconView.show_all()
        #Gtk HeaderBar
        self.Headerbar = Gtk.HeaderBar()
        self.Headerbar.set_show_close_button(True)
        #self.Headerbar.props.title = self.Path
        self.window.set_titlebar(self.Headerbar)

        #sağ taraf buton
        self.BlueToothButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-floppy")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.BlueToothButton.add(image)
        self.BlueToothButton.connect('clicked', self.test)
        self.Headerbar.pack_end(self.BlueToothButton)

        self.ToggleButton = Gtk.ToggleButton()
        icon = Gio.ThemedIcon(name="gtk-stop")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.ToggleButton.add(image)
        self.Headerbar.pack_end(self.ToggleButton)

        #self.ButtonAdd = Gtk.Button()
        #icon = Gio.ThemedIcon(name="gtk-home")
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        #self.ButtonAdd.add(image)
        #self.Headerbar.pack_end(self.ButtonAdd)
        #Sol tarfataki butonlar

        self.HeaderBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.HeaderBox.get_style_context(), "linked")
        self.spinner = Gtk.Spinner()
        self.HeaderBox.add(self.spinner)
        self.Geri = Gtk.Button()
        self.Geri.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Geri)
        self.Ileri = Gtk.Button()
        self.Ileri.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.HeaderBox.add(self.Ileri)
        self.Headerbar.pack_start(self.HeaderBox)
        #sağ taraftaki butonlar
        self.GoEntry = Gtk.Entry()
        self.GoEntry.set_width_chars(50)
        self.GoEntry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY,'gtk-apply')
        self.GoEntry.connect("changed", self.ChangedGoEntry)
        #self.Headerbar.pack_end(self.GoEntry)
        self.FormBox = Gtk.Box(homogeneous=False, spacing=0)
        self.window.add(self.FormBox)
        self.PlacesStore = Gtk.ListStore(str, str)
        self.PlacesStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        for addplaces in LoadPlaces().keys():
            self.PlacesStore.append([addplaces, pdict[addplaces]['icon']])
        self.PlacesTreeView = Gtk.TreeView(self.PlacesStore)
        self.PlacesColumn = Gtk.TreeViewColumn('Konumlar'+' '*30)
        self.PlacesTreeView.append_column(self.PlacesColumn)
        self.CellIcon = Gtk.CellRendererPixbuf()
        self.CellText = Gtk.CellRendererText()
        self.PlacesTreeView.set_property("enable-search", True)
        self.CellText.set_fixed_size(24,24)
        #self.PlacesColumn.set_alignment(10.0)
        #self.CellText.set_property('xalign', 100)
        #self.CellText.set_property('yalign', 0)
        #self.CellText.set_property('wrap-width', 1660)
        #self.CellIcon.set_property('yalign', 100)
        #self.CellText.set_property('editable', True)
        #self.PlacesColumn.set_property('clickable', True)
        #self.CellIcon.set_property('xalign', 0.1)
        #self.CellText.set_property('xalign', 1.0)
        #self.CellText.props.weight_set = True
        #self.CellText.props.weight = Pango.WEIGHT_NORMAL=545 #WEIGHT_BOLD=700
        #self.CellText.props.weight = Pango.Weight.BOLD
        #self.CellText.props.wrap_width = 70  
        #self.CellText.set_property("editable", True)
        self.PlacesColumn.pack_start(self.CellIcon, False)
        self.PlacesColumn.pack_start(self.CellText, True)
        self.PlacesColumn.set_attributes(self.CellIcon, stock_id=1)
        self.PlacesColumn.set_attributes(self.CellText, text=0)
        self.PlacesTreeView.set_activate_on_single_click(True) 
        self.FormBox.add(self.PlacesTreeView)

        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.FormBox.pack_start(self.box2, 1, 1, 0)

        #self.HeaderBar2 = Gtk.HeaderBar()
        #self.box2.add(self.HeaderBar2)

        self.IconViewStatusbar = Gtk.Statusbar()
        self.Info = Gtk.Label()
        self.Info.set_text('kkkkkk')
        self.IconViewStatusbar.add(self.Info)
        #self.box2.add(self.IconViewStatusbar)

        self.IconViewMenuBar = Gtk.MenuBar()
        self.IconViewInfoLabel = Gtk.MenuItem()
        self.IconViewMenuBar.append(self.IconViewInfoLabel)
        self.box2.add(self.IconViewMenuBar)

        #self.ToggleButton = Gtk.ToggleButton()
        #icon = Gio.ThemedIcon(name="gtk-stop")
        #image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        #self.ToggleButton.add(image)
        #self.HeaderBar2.pack_start(self.ToggleButton)

        self.ScrolledWindow = Gtk.ScrolledWindow()
        self.ScrolledWindow.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        self.ScrolledWindow.set_policy(Gtk.PolicyType.AUTOMATIC,
                      Gtk.PolicyType.AUTOMATIC)
        self.box2.pack_end(self.ScrolledWindow, 1, 1, 0)

        self.IconViewStore = Gtk.ListStore(str, str, GdkPixbuf.Pixbuf, bool)
        #self.IconViewStore.set_sort_column_id(0, Gtk.SortType.ASCENDING)
        self.LoadIconView(self.IconViewStore)
        self.IconView = Gtk.IconView(model=self.IconViewStore)
        self.IconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
        self.IconView.set_text_column(self.FILENAME)
        self.IconView.set_pixbuf_column(self.FILEICON)
        self.IconView.set_item_width(self.IconWidth)
        self.IconView.set_margin(5)
        #self.IconView.set_markup_column(5)
        #self.IconView.set_reorderable(100)
        self.IconView.set_row_spacing(0)
        #self.IconView.set_spacing(100)
        #self.IconView.set_border_width(10)
        self.IconView.set_margin_left(0)
        self.IconView.set_margin_right(0)
        self.IconView.set_margin_start(0)
        self.IconView.set_margin_top(0)
        self.IconView.set_opacity(1.0)
        #self.IconView.set_valign(1)
        #self.IconView.set_visible(1)
        self.ScrolledWindow.add(self.IconView)

        self.IconView.grab_focus()
        self.ToggleButton.connect("toggled", self.HideFileShow, self.IconViewStore, '1')
        self.PlacesTreeView.connect('button_press_event', self.PlacesTreeViewSelect, self.PlacesTreeView)
        self.PlacesTreeView.connect('button_press_event', self.LoadPlacesTreeViewSelect, self.IconViewStore)
        self.CellText.connect("edited", self.ChangePlaces)
        self.IconView.connect('selection-changed', self.IconViewSelect, self.IconView) 
        self.IconView.connect('button_press_event', self.IconViewSelectPressEvent, self.IconView)
        self.IconView.connect('button_press_event', self.denemedeneme, self.IconView) ##sil
        self.IconView.connect('item-activated', self.IconViewDoubleClick, self.IconViewStore)
        self.Geri.connect('button-press-event', self.FileBack, self.IconViewStore) 
        self.Ileri.connect('button-press-event', self.FileNext, self.IconViewStore) 
        self.Geri.set_sensitive(False)
        self.Ileri.set_sensitive(False)
        self.window.show_all()

    def on_response(self, widget, response_id):
        self.IconViewStore[self.IconViewSelectIndex][1] = self.IconViewChangeText.get_text()
        isdir = filedict[int(str(self.IconViewSelectIndex))]['isdir']
        OldFile = filedict[int(str(self.IconViewSelectIndex))]['file']
        NewFile = self.Path+'/'+self.IconViewChangeText.get_text()
        os.rename(OldFile, self.Path+'/'+self.IconViewChangeText.get_text())
        filedict[int(str(self.IconViewSelectIndex))] = {'isdir':isdir, 
                            'file':self.Path+'/'+self.IconViewChangeText.get_text()}
        widget.destroy()
    def test(self, BlueToothButton):
        print ('Test Butonu')
    def ChangedGoEntry(self, GoEntry, say=0):
        print ('test')
    def ConTextMenuIconView(self):
        self.MenuIconView.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def IconViewSelectPressEvent(self, IconView,  event, IconViewStore):
        try:
            if event.type == Gdk.EventType.BUTTON_PRESS:
                self.path = self.IconView.get_path_at_pos(event.x, event.y)
                if self.path != None and event.button == 1: 
                    print (self.path, 'self')
                elif (event.button == 3):
                    isdir = os.path.isdir(os.path.join(self.Path, filedict [ int(str(self.path)) ]['file']))
                    self.SelectIconViewIsdir = isdir
                    self.IconView.select_path(self.path)
                    self.ConTextMenuIconView()
                    if (self.IconViewSelectedItem > 0):
                        self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, True), 
                        (self.MenuIconViewDelete, True),(self.MenuIconViewCopeTasi, True), 
                        (self.MenuIconViewCut, True),(self.MenuIconViewPaste, False),
                        (self.MenuIconViewCopy,True), (self.MenuIconViewYeniKlasor,False), 
                        (self.MenuIconViewFolderAddPlaces,True)])
                    else:
                        self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, True), 
                        (self.MenuIconViewDelete, True),(self.MenuIconViewCopeTasi, True),
                        (self.MenuIconViewCut, True),
                        (self.MenuIconViewCopy,True), (self.MenuIconViewPaste, False)
                        (self.MenuIconViewYeniKlasor,False), 
                        (self.MenuIconViewFolderAddPlaces,False)])
        except:
            self.ConTextMenuIconView()
            if (len(self.ExtendSelectIconViewIndex) is 0):
                self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, False), 
                (self.MenuIconViewDelete, False),
                (self.MenuIconViewCopeTasi, False),
                (self.MenuIconViewCut, False),
                (self.MenuIconViewCopy,False), 
                (self.MenuIconViewPaste, False),
                (self.MenuIconViewYeniKlasor,True),
                (self.MenuIconViewFolderAddPlaces,False)])
            else:
                self.IconViewContextMenuEnabled([(self.MenuIconViewChanged, False), 
                (self.MenuIconViewDelete, False),
                (self.MenuIconViewCopeTasi, False),
                (self.MenuIconViewCut, False),
                (self.MenuIconViewCopy,False), 
                (self.MenuIconViewPaste, True),
                (self.MenuIconViewYeniKlasor,True),
                (self.MenuIconViewFolderAddPlaces,False)])
    def IconViewContextMenuEnabled(self, menuitem):
        for enabled in menuitem:
            enabled[0].set_sensitive(enabled[1])
    def denemedeneme(self, IconView, Event, IconViewStore):
        if Event.button == 3:
            pthinfo = self.IconView.get_path_at_pos(Event.x, Event.y)
            self.IconViewSelectIndex = pthinfo
    def IconViewSelect(self, IconView, event, model=None):
        self.IconViewSelectedItem = IconView.get_selected_items()
        if (len(self.IconViewSelectedItem) is 0):
            info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
            self.StatusBarInfo(info) 
        else:
            string = str(len(self.IconViewSelectedItem)) + ' Dosya seçildi'
            self.StatusBarInfo(string)
        #for test in  self.IconViewSelectedItem:
        #    print test
        #print (filedict)
    def IconViewFonksiyon(self, PlacesTreeView, data = None):
        selection = self.PlacesTreeView.get_selection()
        (model, iter) = selection.get_selected()
        if (data == 'Gdeb'):
            #SelectDebFiles = []
            for SelectDebAppend in self.IconViewSelectedItem:
                SelectDebFiles.append(filedict[int(str(SelectDebAppend))]['file'])
            SelectDebFiles.append(self.Path)
            FileOptions(self)
        if (data == 'Yeni Klasör'):
            for id in range(1, 111):
                Error = os.path.isdir(self.Path +'/'+ self.DefaultFolder + str(id))
                if (Error is True):
                    continue
                if (Error is False):
                    print(id, 'yeni klasör')
                    self.DefaultFolder = self.DefaultFolder + str(id)
                    os.makedirs(self.Path +'/'+ self.DefaultFolder)
                    self.IconViewStore.append((os.path.join(self.Path, 
                        self.DefaultFolder),self.DefaultFolder, 
                        self.FileIcon(os.path.join(self.Path, 
                            self.DefaultFolder)),
                    os.path.isdir(os.path.join(self.Path, 
                        self.DefaultFolder))
                        )
                    )
                    NewFolder = self.DefaultFolder
                    isdir = os.path.isdir(os.path.join(self.Path, NewFolder))
                    filedict[len(filedict)] = {'isdir':isdir, 'file':self.Path+'/'+NewFolder}
                    break
        if (data == 'Konuma Ekle'):
            keys = os.path.split ( filedict [ int(str(self.path)) ]['file'] )[1]
            path = filedict [ int(str(self.path)) ]['file']
            #icon = filedict [ int(str(self.path)) ]['icon']
            self.PlacesStore.append([keys, 'gtk-home'])
            pdict[keys] = {'path':path, 'icon':'gtk-home', 'main':'False'}
            ConfigAddPlaces(path,keys,'gtk-home','False')
        if (data == 'Sil'):
            #https://www.linux.com/blog/linux-shell-tip-remove-files-names-contains-spaces-and-special-characters-such
            for delete in self.IconViewSelectedItem:
                self.spinner.start()
                if filedict[int(str(delete))]['isdir'] is True:
                    self.Info = os.system('rm -r '+filedict[int(str(delete))]['file'].replace(' ', '\ ')) #klasor
                    self.CountFolder = self.CountFolder -1
                else: 
                    self.Info = os.system('rm -f '+filedict[int(str(delete))]['file'].replace(' ', '\ '))
                    self.CountText = self.CountText -1
                self.IconViewStore.remove(self.IconViewStore.get_iter(delete))
                for test in range(int(str(delete)), len(filedict)):
                    if test is not len(filedict)-1:
                        filedict[test] = filedict[test+1]
                    else:
                        filedict.pop(test)
            info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
            self.StatusBarInfo(info) 
            self.spinner.stop()
        if (data == 'Yeniden Adlandır'):
            print ('Yeniden Adlandır')
            self.IconViewChangeDialog = Gtk.Dialog()
            self.IconViewChangeDialog.set_title("Yeniden Adlandır")
            self.IconViewChangeDialog.set_transient_for(self)
            self.IconViewChangeDialog.set_modal(True)
            self.IconViewChangeDialog.add_button(button_text="Tamam", response_id=Gtk.ResponseType.OK)
            self.IconViewChangeDialog.add_button(button_text="Iptal", response_id=Gtk.ResponseType.CANCEL)
            self.IconViewChangeDialog.connect("response", self.on_response)
            content_area = self.IconViewChangeDialog.get_content_area()
            self.IconViewChangeLabel = Gtk.Label()
            self.IconViewChangeLabel.set_text('Dosya Adı:'+ ' '*35)
            self.IconViewChangeText = Gtk.Entry()
            self.IconViewChangeText.set_width_chars(20)
            self.IconViewChangeText.set_text(os.path.split(filedict[int(str(self.IconViewSelectIndex))]['file'])[1])
            content_area.add(self.IconViewChangeLabel)
            content_area.add(self.IconViewChangeText)
            self.IconViewChangeDialog.show_all()

        if (data == 'BlueTooth ile Gönder'):
            print ('Bluetooth')

        if (data == 'Çöp Kutusuna Taşı'):
            for TrashMove in self.IconViewSelectedItem:
                os.system('mv '+filedict[int(str(TrashMove))]['file'] +' '+ self.RashPath)
                self.IconViewStore.remove(self.IconViewStore.get_iter(TrashMove))

        if (data == 'Kopyala'):
            print ('kopyalama işlemi', self.IconViewSelectedItem)
            self.IcinViewSelectOptions = 'Kopyala'
            self.ExtendSelectIconViewIndex, self.ExtendSelectIconViewFile = [], []
            for test in self.IconViewSelectedItem:
                self.ExtendSelectIconViewIndex.extend(test)
            for test in self.ExtendSelectIconViewIndex:
                self.ExtendSelectIconViewFile.extend([filedict[int(str(test))]['file'].replace(' ','\ ')])

        if (data == 'Taşı'):
            print ('taşıma işlemi', self.IconViewSelectedItem)
            self.IcinViewSelectOptions = 'Taşı'
            self.ExtendSelectIconViewIndex, self.ExtendSelectIconViewFile = [], []
            for test in self.IconViewSelectedItem:
                self.ExtendSelectIconViewIndex.extend(test)
            for test in self.ExtendSelectIconViewIndex:
                self.ExtendSelectIconViewFile.extend([filedict[int(str(test))]['file'].replace(' ','\ ')])

        if (data == 'Yapıştır'):
            if (self.IcinViewSelectOptions == 'Kopyala'):
                print('kopyala geliştiriliyor.')
                for source in self.ExtendSelectIconViewFile:
                    c1 = CopyCut(source, self.Path.replace(' ','\ '))
                    c1.start()
            elif (self.IcinViewSelectOptions == 'Taşı'):
                print ('Taşı')
                for source in self.ExtendSelectIconViewFile:
                    os.system('mv ' + source + ' ' + self.Path.replace(' ', '\ '))
                    self.IconViewStore.clear()
                    self.LoadIconView(self.IconViewStore)
                    isdir = os.path.isdir(os.path.join(self.Path, source))
                    filedict[len(filedict)] = {'isdir':isdir, 'file':self.Path+'/'+source}

    def HideFileShow(self, ToggleButton, IconViewStore, name):
        if self.ToggleButton.get_active():
            self.state = True
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
        else:
            self.state = False
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
    def ChangePlaces(self, widget, path, text):
        with open(PlacesSource) as read:
            source = read.read()
        source = source.replace(pdict[self.PlacesStore[path][0]]['path']+','+self.PlacesStore[path][0], 
            pdict[self.PlacesStore[path][0]]['path']+','+text)
        with open(PlacesSource, 'w') as change:
            change.write(source)
        self.PlacesStore[path][0] = text
        self.CellText.set_property("editable", False)
        pdict[text] = self.SelectPlacesItemChangePdict
    def PlacesTreeViewFonksiyon(self, PlacesTreeView, data = None):
        selection = self.PlacesTreeView.get_selection()
        (model, iter) = selection.get_selected()
        if (data == 'Sil'):
            ConfigDeletePlaces(pdict[model[self.SelectPlacesItemIter][0]]['path']+','+model[self.SelectPlacesItemIter][0])
            model.remove(self.SelectPlacesItemIter)
        elif (data == 'Yeniden Adlandır'):
            self.CellText.set_property("editable", True)
            self.SelectPlacesItemChangePdict = pdict[model[iter][0]]
    def PlacesTreeViewSelect(self, PlacesTreeView, Event, PlacesStore):
        if Event.button == 3:
            pthinfo = self.PlacesTreeView.get_path_at_pos(Event.x, Event.y)
            if pthinfo != None:
                (path,col,cellx,celly) = pthinfo
                self.PlacesTreeView.grab_focus()
                self.PlacesTreeView.set_cursor(path, col, 0)
            selection = self.PlacesTreeView.get_selection()
            (model, iter) = selection.get_selected()
            self.SelectPlacesItemIter = iter
            if (pdict[model[iter][0]]['main'] == 'False'): 
                self.menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
    def LoadPlacesTreeViewSelect(self, PlacesTreeView, Event, IconViewStore):  
        if Event.button == 1:
            pthinfo = self.PlacesTreeView.get_path_at_pos(Event.x, Event.y)
            if pthinfo != None:
                (path,col,cellx,celly) = pthinfo
                self.PlacesTreeView.grab_focus()
                self.PlacesTreeView.set_cursor(path,col,0)
            selection = self.PlacesTreeView.get_selection()
            (model, iter) = selection.get_selected()
            self.SelectPlacesItem = pdict[model[iter][0]]['path']
            self.Path = self.SelectPlacesItem
            #self.Headerbar.props.title = self.Path
            TempWrite(self.Path)
            self.Geri.set_sensitive(True)
            self.ArrayNextBack.append(self.Path)
            self.CountNextBack = self.CountNextBack + 1
            #print (self.ArrayNextBack)
            self.IconViewStore.clear()
            self.LoadIconView(self.IconViewStore)
            if (self.Path == HOME+'/.local/share/Trash/files/'):
                self.GoEntry.set_text('Rash://')
    def FileBack(self, IconView, path, IconViewStore):
        if self.CountNextBack > 1: self.CountNextBack = self.CountNextBack - 1
        if self.CountNextBack is 1 :             
            self.Geri.set_sensitive(False
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        if len(self.ArrayNextBack) > self.CountNextBack:
            self.Ileri.set_sensitive(True)
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        #self.Headerbar.props.title = self.Path
        TempWrite(self.Path)
    def FileNext(self, IconView, path, IconViewStore):
        self.CountNextBack = self.CountNextBack + 1
        if self.CountNextBack is len(self.ArrayNextBack) :             
            self.Ileri.set_sensitive(False
                )
        if self.CountNextBack > 1 :             
            self.Geri.set_sensitive(True
                )
        self.Path = self.ArrayNextBack[self.CountNextBack-1]
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        #self.Headerbar.props.title = self.Path
        TempWrite(self.Path)
    def IconViewDoubleClick(self, IconView, tree_path, IconViewStore):
        iter_ = self.IconViewStore.get_iter(tree_path)
        (path, is_dir) = self.IconViewStore.get(iter_, self.COL_PATH, self.COL_IS_DIRECTORY)
        if (is_dir is True) : 
            TempWrite(path)
            self.ArrayNextBack.insert(self.CountNextBack, path)
            self.CountNextBack = self.CountNextBack + 1
        else:
            subprocess.call(('xdg-open', path))
        if not is_dir:
            return
        self.Path = path
        #self.Headerbar.props.title = self.Path
        self.IconViewStore.clear()
        self.LoadIconView(self.IconViewStore)
        if len(self.ArrayNextBack) > 1:
            self.Geri.set_sensitive(True
                )
    def LoadIconView(self, IconViewStore, indextest=0): 
        print 'StUid:', os.stat(self.Path).st_uid

        self.CountFolder, self.CountText, self.CountHideFile = 0, 0, 0
        self.GoEntry.set_text(self.Path)
        try:
            if (self.Path == HOME+'/.local/share/Trash/files/'):
                self.GoEntry.set_text('Rash://')
            for enum, FileName in enumerate(os.listdir(self.Path),0):
                if FileName.startswith('.') is True and self.state is False:
                        indextest = indextest + 1
                        self.CountHideFile = self.CountHideFile + 1
                        continue
                filedict[enum-indextest] = {'file':self.Path+'/'+FileName, 
                        'isdir':os.path.isdir(os.path.join(self.Path, FileName))}
                if os.path.isdir(os.path.join(self.Path, FileName)) is True:
                    self.CountFolder = self.CountFolder + 1
                else:
                    self.CountText = self.CountText + 1
                self.IconViewStore.append(
                (os.path.join(self.Path, FileName), 
                    FileName, 
                    self.FileIcon(os.path.join(self.Path, FileName)
                        ),
                    os.path.isdir(os.path.join(self.Path, FileName)
                        )
                    )
                )
            if (self.CountFolder is 0 and self.CountText is 0):
                self.StatusBarInfo(str('Dizin boş'))
            else:
                info = str(self.CountFolder)+' Dizin, '+str(self.CountText)+' Dosya, '+str(self.CountHideFile)+' Gizli'
                self.StatusBarInfo(info) 
        except:
            self.StatusBarInfo(str('Böyle bir dizin yok'))   
    def StatusBarInfo(self, String):
        StatusBarInfo = String
        self.IconViewInfoLabel.set_label(str(StatusBarInfo))
        self.IconViewInfoLabel.select()
        self.IconViewInfoLabel.activate()
    def FileIcon(self, path):
        fileicon = None
        giopath = Gio.file_new_for_path(path)
        query = giopath.query_info(Gio.FILE_ATTRIBUTE_STANDARD_ICON,
            Gio.FileQueryInfoFlags.NONE,
                    None)
        geticonnames = query.get_icon().get_names()
        icontheme = Gtk.IconTheme.get_default()
        for icon in geticonnames:
            try:
                fileicon = icontheme.load_icon(icon, 64, 0)
                break
            except GLib.GError:
                pass
        return fileicon

def main(BetaApp=None):
    BetaFileManager(BetaApp)
    Gtk.main()
if __name__ == '__main__':
    main()

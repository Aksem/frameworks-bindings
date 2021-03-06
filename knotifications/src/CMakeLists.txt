if (Phonon4Qt5_FOUND)
    include_directories(${PHONON_INCLUDE_DIR})
endif()

ecm_create_qm_loader(knotifications_QM_LOADER knotifications5_qt)

set(knotifications_SRCS

  knotification.cpp
  knotificationmanager.cpp
  kpassivepopup.cpp
  kstatusnotifieritem.cpp
  kstatusnotifieritemdbus_p.cpp
  knotificationrestrictions.cpp

  knotifyconfig.cpp
  knotificationplugin.cpp
  notifybypopup.cpp
  imageconverter.cpp #needed to marshal images for sending over dbus by NotifyByPopup
  notifybypopupgrowl.cpp
  notifybyexecute.cpp
#   notifybylogfile.cpp
  notifybytaskbar.cpp
  ${knotifications_QM_LOADER}
)

ecm_qt_declare_logging_category(knotifications_SRCS HEADER debug_p.h IDENTIFIER LOG_KNOTIFICATIONS CATEGORY_NAME org.kde.knotifications)

if (Phonon4Qt5_FOUND)
  set(knotifications_SRCS ${knotifications_SRCS}
  notifybyaudio.cpp)
endif()

if (Qt5TextToSpeech_FOUND)
  set(knotifications_SRCS ${knotifications_SRCS}
    notifybytts.cpp)
endif()

find_package(dbusmenu-qt5 CONFIG)
set_package_properties(dbusmenu-qt5 PROPERTIES DESCRIPTION "DBusMenuQt"
                       URL "https://launchpad.net/libdbusmenu-qt" TYPE OPTIONAL
                       PURPOSE "Support for notification area menus via the DBusMenu protocol")
if (dbusmenu-qt5_FOUND)
   message("dbusmenu-qt5_FOUND")
   set(HAVE_DBUSMENUQT 1)
   include_directories(${dbusmenu-qt5_INCLUDE_DIRS})
else()
   set(HAVE_DBUSMENUQT 0)
endif()

qt5_add_dbus_adaptor(knotifications_SRCS     org.kde.StatusNotifierItem.xml
                     kstatusnotifieritemdbus_p.h KStatusNotifierItemDBus)


set(statusnotifierwatcher_xml org.kde.StatusNotifierWatcher.xml)
qt5_add_dbus_interface(knotifications_SRCS ${statusnotifierwatcher_xml} statusnotifierwatcher_interface)
set(notifications_xml org.freedesktop.Notifications.xml)
qt5_add_dbus_interface(knotifications_SRCS ${notifications_xml} notifications_interface)

configure_file(config-knotifications.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config-knotifications.h )

add_library(KF5Notifications ${knotifications_SRCS})
generate_export_header(KF5Notifications BASE_NAME KNotifications)
add_library(KF5::Notifications ALIAS KF5Notifications)

target_include_directories(KF5Notifications INTERFACE "$<INSTALL_INTERFACE:${KDE_INSTALL_INCLUDEDIR_KF5}/KNotifications>")

target_link_libraries(KF5Notifications PUBLIC
   Qt5::Widgets
)
target_link_libraries(KF5Notifications PRIVATE
   KF5::CoreAddons
   KF5::ConfigCore
   KF5::WindowSystem
   KF5::Codecs
   Qt5::DBus
)

if (Phonon4Qt5_FOUND)
    target_link_libraries(KF5Notifications PRIVATE
        ${PHONON_LIBRARIES})
endif()

if (Qt5TextToSpeech_FOUND)
    target_link_libraries(KF5Notifications PRIVATE Qt5::TextToSpeech)
endif()

if(X11_FOUND)
   target_link_libraries(KF5Notifications PRIVATE ${X11_X11_LIB} Qt5::X11Extras)
endif()

if(X11_XTest_FOUND)
  target_link_libraries(KF5Notifications PRIVATE ${X11_XTest_LIB})
endif()

if(HAVE_DBUSMENUQT)
  target_link_libraries(KF5Notifications PRIVATE dbusmenu-qt5)
endif()

set_target_properties(KF5Notifications PROPERTIES VERSION   ${KNOTIFICATIONS_VERSION_STRING}
                                                  SOVERSION ${KNOTIFICATIONS_SOVERSION}
                                                  EXPORT_NAME Notifications
)

ecm_generate_headers(KNotifications_HEADERS
  HEADER_NAMES
  KNotification
  KPassivePopup
  KStatusNotifierItem
  KNotificationRestrictions
  KNotificationPlugin
  KNotifyConfig

  REQUIRED_HEADERS KNotifications_HEADERS
)

find_package(PythonModuleGeneration)

if (PythonModuleGeneration_FOUND)
  ecm_generate_python_binding(
    TARGET KF5::Notifications
    PYTHONNAMESPACE PyKF5
    MODULENAME KNotifications
    RULES_FILE "${CMAKE_SOURCE_DIR}/cmake/rules_PyKF5.py"
    SIP_INCLUDES $<TARGET_PROPERTY:Qt5::Widgets,INTERFACE_INCLUDE_DIRECTORIES> #?
    SIP_DEPENDS
      QtCore/QtCoremod.sip
      QtWidgets/QtWidgetsmod.sip
      PyKF5/KCoreAddons/KCoreAddonsmod.sip
      PyKF5/KConfigCore/KConfigCoremod.sip
    HEADERS
      ${KNotifications_HEADERS}
  )
endif()

install(TARGETS KF5Notifications EXPORT KF5NotificationsTargets ${KF5_INSTALL_TARGETS_DEFAULT_ARGS})

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/knotifications_export.h
  ${KNotifications_HEADERS}
  DESTINATION ${KDE_INSTALL_INCLUDEDIR_KF5}/KNotifications COMPONENT Devel
)

install(FILES
    org.kde.StatusNotifierItem.xml
    DESTINATION ${KDE_INSTALL_DBUSINTERFACEDIR}
    RENAME kf5_org.kde.StatusNotifierItem.xml)

install(FILES
    org.kde.StatusNotifierWatcher.xml
    DESTINATION ${KDE_INSTALL_DBUSINTERFACEDIR}
    RENAME kf5_org.kde.StatusNotifierWatcher.xml)

install(FILES
    knotificationplugin.desktop
    DESTINATION ${KDE_INSTALL_KSERVICETYPES5DIR})

include(ECMGeneratePriFile)
ecm_generate_pri_file(BASE_NAME KNotifications LIB_NAME KF5Notifications DEPS "widgets" FILENAME_VAR PRI_FILENAME INCLUDE_INSTALL_DIR ${KDE_INSTALL_INCLUDEDIR_KF5}/KNotifications)
install(FILES ${PRI_FILENAME} DESTINATION ${ECM_MKSPECS_INSTALL_DIR})


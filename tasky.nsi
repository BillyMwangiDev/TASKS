; TASKY Windows Installer — NSIS script
; Produces: TASKY-Setup-v2.0.0.exe

!define APP_NAME    "TASKY"
!define APP_VERSION "2.0.0"
!define INSTALLER   "TASKY-Setup-v${APP_VERSION}.exe"
!define INSTALL_DIR "$PROGRAMFILES64\${APP_NAME}"
!define REG_KEY     "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"

Name            "${APP_NAME} ${APP_VERSION}"
OutFile         "${INSTALLER}"
InstallDir      "${INSTALL_DIR}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Modern UI
!include "MUI2.nsh"
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File /r "dist\TASKY\*.*"

    ; Registry — install path + uninstaller entry
    WriteRegStr  HKLM "Software\${APP_NAME}" "Install_Dir" "$INSTDIR"
    WriteRegStr  HKLM "${REG_KEY}" "DisplayName"          "${APP_NAME} ${APP_VERSION}"
    WriteRegStr  HKLM "${REG_KEY}" "DisplayVersion"       "${APP_VERSION}"
    WriteRegStr  HKLM "${REG_KEY}" "Publisher"            "TASKY"
    WriteRegStr  HKLM "${REG_KEY}" "UninstallString"      '"$INSTDIR\Uninstall.exe"'
    WriteRegDWORD HKLM "${REG_KEY}" "NoModify" 1
    WriteRegDWORD HKLM "${REG_KEY}" "NoRepair" 1
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Start Menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"  "$INSTDIR\TASKY.exe"
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"    "$INSTDIR\Uninstall.exe"

    ; Desktop shortcut
    CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\TASKY.exe"
SectionEnd

Section "Uninstall"
    RMDir /r "$INSTDIR"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir  "$SMPROGRAMS\${APP_NAME}"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    DeleteRegKey HKLM "${REG_KEY}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
SectionEnd

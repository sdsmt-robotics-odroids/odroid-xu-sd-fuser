Name:           odroid-xu-sd-fuser
Version:        0.1.0
Release:        1%{?dist}
Summary:        Boot media blob for ODROID-XU

Group:          System Environment/Base
License:        BSD
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-xu
Source0:        https://github.com/hardkernel/linux/raw/odroidxu-3.4.y/tools/hardkernel/u-boot-pre-built/bl1.hardkernel.bin.signed
Source1:        https://github.com/hardkernel/linux/raw/odroidxu-3.4.y/tools/hardkernel/u-boot-pre-built/bl2.hardkernel.bin.signed
Source2:        https://github.com/hardkernel/linux/raw/odroidxu-3.4.y/tools/hardkernel/u-boot-pre-built/tzsw.hardkernel.bin.signed
Source3:        odroid-xu-sd-fuser
Source4:        odroid-xu-emmc-fuser

BuildArch:      noarch

BuildRequires:  odroid-xu-uboot

%description
Binary blob used to boot Hardkernel's ODROID-XU. The blob contains:
- bl1
- bl2
- u-boot
- TrustZone

%prep
cp -a %{SOURCE3} odroid-xu-sd-fuser
cp -a %{SOURCE4} odroid-xu-emmc-fuser

%build
signed_bl1_position=0
bl2_position=30
uboot_position=62
tzsw_position=718

#<BL1 fusing>
echo "BL1 fusing"
dd oflag=dsync if=%{SOURCE0} of=bootblob.bin seek=$signed_bl1_position
#<BL2 fusing>
echo "BL2 fusing"
dd if=%{SOURCE1} of=bootblob.bin seek=$bl2_position
#<u-boot fusing>
echo "u-boot fusing"
dd if=/boot/uboot/u-boot.bin of=bootblob.bin seek=$uboot_position
#<TrustZone S/W fusing>
echo "TrustZone S/W fusing"
dd if=%{SOURCE2} of=bootblob.bin seek=$tzsw_position

chmod +x bootblob.bin

sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-xu-sd-fuser
sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-xu-emmc-fuser

%install
install -p -m0755 -D bootblob.bin %{buildroot}%{_datadir}/%{name}/bootblob.bin
install -p -m0755 -D odroid-xu-sd-fuser %{buildroot}%{_bindir}/odroid-xu-sd-fuser
install -p -m0755 -D odroid-xu-emmc-fuser %{buildroot}%{_bindir}/odroid-xu-emmc-fuser

%files
%{_bindir}/odroid-xu-sd-fuser
%{_bindir}/odroid-xu-emmc-fuser
%{_datadir}/%{name}/bootblob.bin

%changelog
* Sat Apr 04 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package

PERL_MODULES := perl-modules

PERL_MODULES_BUILD := $(BUILD_HELPER_DIR)/$(PERL_MODULES)-build
PERL_MODULES_INTERMEDIATE_INSTALL := $(BUILD_HELPER_DIR)/$(PERL_MODULES)-install-intermediate
PERL_MODULES_INSTALL := $(BUILD_HELPER_DIR)/$(PERL_MODULES)-install

PERL_MODULES_INSTALL_DIR := $(INTERMEDIATE_INSTALL_BASE)/$(PERL_MODULES)
PERL_MODULES_TAR := $(BAZEL_BIN)/omd/packages/$(PERL_MODULES)/$(PERL_MODULES).tar
PERL_MODULES_WORK_DIR := $(PACKAGE_WORK_DIR)/$(PERL_MODULES)

PERL_MODULES_BUILD_PERL5LIB := $(PERL_MODULES_INSTALL_DIR)/lib/perl5

# Used by other packages
PACKAGE_PERL_MODULES_PERL5LIB := $(PERL_MODULES_INSTALL_DIR)/lib/perl5

$(PERL_MODULES_BUILD):
	$(BAZEL_BUILD) //omd/packages/$(PERL_MODULES):$(PERL_MODULES)

$(PERL_MODULES_INTERMEDIATE_INSTALL): $(PERL_MODULES_BUILD)
	$(MKDIR) $(PERL_MODULES_INSTALL_DIR)/lib/perl5 $(PERL_MODULES_INSTALL_DIR)/bin
	tar --strip-components 1 -xf $(PERL_MODULES_TAR) -C $(PERL_MODULES_BUILD_PERL5LIB)
	$(MKDIR) $(PERL_MODULES_INSTALL_DIR)/local/lib/perl5
	install -m 755 $(PACKAGE_DIR)/$(PERL_MODULES)/bin/cpan.wrapper $(PERL_MODULES_INSTALL_DIR)/bin/cpan.wrapper
# Fixup some library permissions. They need to be owner writable to make
# dh_strip command of deb packaging procedure work
	find $(PACKAGE_PERL_MODULES_PERL5LIB) -type f -name \*.so -exec chmod u+w {} \;
	find $(PACKAGE_PERL_MODULES_PERL5LIB) -type f -name \*.pm -exec chmod -x {} \;
	cd $(PERL_MODULES_BUILD_PERL5LIB) ; $(RM) utils.pm ; ln -s ../../../nagios/plugins/utils.pm .
	$(MKDIR) $(PERL_MODULES_BUILD_PERL5LIB)/CPAN
	cp $(PACKAGE_DIR)/$(PERL_MODULES)/MyConfig.pm $(PERL_MODULES_BUILD_PERL5LIB)/CPAN/MyConfig.skel
	$(TOUCH) $@

$(PERL_MODULES_INSTALL): $(PERL_MODULES_INTERMEDIATE_INSTALL)
	$(RSYNC) $(PERL_MODULES_INSTALL_DIR)/ $(DESTDIR)$(OMD_ROOT)/
	echo "install  --install_base  ###ROOT###/local/lib/perl5" > $(SKEL)/.modulebuildrc
	$(TOUCH) $@

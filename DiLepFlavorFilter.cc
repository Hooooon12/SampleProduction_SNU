// -*- C++ -*-
//
// Package:    FourLepFilter
// Class:      FourLepFilter
//
/**\class FourLepFilter FourLepFilter.cc psi2s1s/FourLepFilter/src/FourLepFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  bian jianguo
//         Created:  Tue Nov 22 20:39:54 CST 2011
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"

#include <iostream>

//
// class declaration
//

class DiLepFlavorFilter : public edm::EDFilter {
public:
  explicit DiLepFlavorFilter(const edm::ParameterSet&);
  ~DiLepFlavorFilter() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  // ----------member data ---------------------------

  edm::EDGetToken token_;
  bool SF_, DF_; 
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
DiLepFlavorFilter::DiLepFlavorFilter(const edm::ParameterSet& iConfig)
    : token_(consumes<LHEEventProduct>(iConfig.getUntrackedParameter<edm::InputTag>("src"))),
      SF_(iConfig.getParameter<bool>("SF")),
      DF_(iConfig.getParameter<bool>("DF")) {}

DiLepFlavorFilter::~DiLepFlavorFilter() {
  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)
}

//
// member functions
//

// ------------ method called on each new Event  ------------
bool DiLepFlavorFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  int LepFlavor = 1; //JH : 1 for mu, -1 for e

  Handle<LHEEventProduct> evt;
  iEvent.getByToken(token_, evt);
  const lhef::HEPEUP& lheEvent = evt->hepeup();
  std::vector<lhef::HEPEUP::FiveVector> lheParticles = lheEvent.PUP;

  for( size_t idxParticle = 0; idxParticle < lheParticles.size(); ++idxParticle )
  {
    int id = lheEvent.IDUP[idxParticle];

    if (id==11||id==-11) LepFlavor *= -1;
    else if (id==13||id==-13) LepFlavor *= 1;
  }

  if (LepFlavor > 0 && SF_)
    return true;
  else if (LepFlavor < 0 && DF_)
    return true;
  else
    return false;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void DiLepFlavorFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(DiLepFlavorFilter);

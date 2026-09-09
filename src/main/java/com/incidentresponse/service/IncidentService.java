package com.incidentresponse.service;

import com.incidentresponse.entity.Incident;
import com.incidentresponse.exception.ResourceNotFoundException;
import com.incidentresponse.repository.IncidentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class IncidentService {

    @Autowired
    private IncidentRepository incidentRepository;

    @Autowired
    private AIAnalysisService aiAnalysisService;

    public Incident createIncident(Incident incident) {
        Map<String, String> result = aiAnalysisService.analyze(
                incident.getAttackType(),
                incident.getFailedAttempts(),
                incident.getTargetAsset()
        );

        incident.setClassification(result.get("classification"));
        incident.setSeverity(result.get("severity"));

        return incidentRepository.save(incident);
    }

    public List<Incident> getAllIncidents() {
        return incidentRepository.findAll();
    }

    public Incident getIncidentById(Long id) {
        return incidentRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Incident not found with id: " + id));
    }

    public Incident updateIncident(Long id, Incident updatedIncident) {
        Incident existing = getIncidentById(id);

        existing.setSourceIp(updatedIncident.getSourceIp());
        existing.setDestinationIp(updatedIncident.getDestinationIp());
        existing.setAttackType(updatedIncident.getAttackType());
        existing.setFailedAttempts(updatedIncident.getFailedAttempts());
        existing.setTargetAsset(updatedIncident.getTargetAsset());
        if (updatedIncident.getStatus() != null) {
            existing.setStatus(updatedIncident.getStatus());
        }

        return incidentRepository.save(existing);
    }

    public void deleteIncident(Long id) {
        Incident existing = getIncidentById(id);
        incidentRepository.delete(existing);
    }

    public List<Incident> getIncidentsByAttackType(String attackType) {
        return incidentRepository.findByAttackType(attackType);
    }

    public List<Incident> getIncidentsByStatus(String status) {
        return incidentRepository.findByStatus(status);
    }
}